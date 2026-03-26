import os
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine, text
from geoalchemy2 import Geometry
import requests
from shapely.geometry import mapping, MultiPolygon
import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="Upload municipality data")
    parser.add_argument("--username", required=True, help="Username for authentication")
    parser.add_argument("--password", required=True, help="Password for authentication")
    return parser.parse_args()


GEOJSON_PATH = os.getenv("GEOJSON_PATH", "/app/data/municipalities_nl.geojson")
CSV_PATH = os.getenv("CSV_PATH", "/app/data/gemeenten-alfabetisch-2026.csv")
BASE_URL = f'http://0.0.0.0:{os.getenv("DJANGO_PORT",8005)}'
AUTH_API = os.getenv("AUTH_API",'/api/token/')
MUNICIPALITIES_API = os.getenv("MUNICIPALITY_API",'/api/municipalities/')
DB_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@db_service:5432/postgres"
)
TABLE_NAME = "quickstart_municipalities"


def get_auth_token(token_url, username, password):
    token_url = token_url
    myobj = {"username": username, "password": password}
    token_response = requests.post(token_url, myobj)

    token_response.raise_for_status()

    # Parse JSON
    token = token_response.json().get("access")
    print("\nUser authenticated successfully with access token: ",token)
    return token


def load_data():
    gdf = gpd.read_file(GEOJSON_PATH).set_crs(4326)
    gdf = gdf.rename_geometry("geom")
    df = pd.read_csv(CSV_PATH)
    return gdf, df


def ensure_multipolygon(geom):
    if geom.geom_type == "Polygon":
        return MultiPolygon([geom])
    return geom


def preprocess(gdf, df):
    df_small = df[["Gemeentenaam", "GemeentecodeGM"]]

    common = set(gdf["name"]).intersection(df_small["Gemeentenaam"])

    gdf = gdf[gdf["name"].isin(common)].copy()
    gdf = gdf.merge(
        df_small.rename(columns={"GemeentecodeGM": "code"}),
        left_on="name",
        right_on="Gemeentenaam",
        how="left",
    ).drop(columns=["Gemeentenaam"])

    return gdf, common


def get_engine():
    return create_engine(DB_URL)


def fetch_existing(engine):
    try:
        return gpd.read_postgis(f"SELECT name, geom FROM {TABLE_NAME}", engine)
    except Exception as e:
        print(f"Warning: Could not fetch existing data: {e}")
        print("Proceeding as if table is empty.")
        return gpd.GeoDataFrame(columns=["name"])


def filter_new_records(gdf, common, existing_gdf):
    existing_names = set(existing_gdf["name"])
    missing = set(common) - existing_names

    if not missing:
        print("\nNo new municipalities to insert.\n")
        return gdf.iloc[0:0]

    gdf = gdf[gdf["name"].isin(missing)].copy()
    print(f"\nInserting {len(gdf)} new municipalities.")

    return gdf


def insert_data(gdf, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    for _, row in gdf.iterrows():
        geom = row.geom
        if geom is None:
            continue

        try:
            geom = ensure_multipolygon(geom)

            payload = {"name": row["name"], "code": row["code"], "geom": mapping(geom)}

            response = requests.post(
                BASE_URL+MUNICIPALITIES_API, json=payload, headers=headers
            )

            if response.status_code != 201:
                print(f"Failed for {row['name']}: {response.text}")
            else:
                print(f"Inserted: {row['name']}")

        except Exception as exc:
            print(f"Skipping '{row['name']}': {exc}")


def sync_sequence(engine):
    with engine.begin() as conn:
        conn.execute(
            text(f"""
            SELECT setval(
                pg_get_serial_sequence('{TABLE_NAME}', 'id'),
                (SELECT COALESCE(MAX(id), 1) FROM {TABLE_NAME})
            );
        """)
        )


def main():
    args = parse_arguments()
    token = get_auth_token(BASE_URL+AUTH_API, args.username, args.password)
    gdf, df = load_data()
    gdf, common = preprocess(gdf, df)

    engine = get_engine()
    existing_gdf = fetch_existing(engine)
    print(f"\nFound {len(existing_gdf)} existing features with the same code as the input geojson")

    gdf_new = filter_new_records(gdf, common, existing_gdf)

    insert_data(gdf_new, token)
    sync_sequence(engine)


if __name__ == "__main__":
    main()
