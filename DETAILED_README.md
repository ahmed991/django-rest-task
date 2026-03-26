# Django REST Framework Task

**Author:** Ahmed Hanif

A Django REST Framework API for managing municipal boundaries in the Netherlands with geospatial capabilities. Uses PostgreSQL with PostGIS for storing and querying geographic data.

---

## Deliverables

| Feature | Status |
|---|---|
| CRUD REST API for GeoJSON Features (paginated, 100/page) |Done|
| Bounding Box Filtering |Done|
| Dataset Integration (NL municipalities loaded into PostGIS) |Done|
| Docker Containerization (Bonus) |Done|
| JWT Authentication (Bonus) |Done|

---

## Data Sources

- **Municipalities CSV** — CBS (Centraal Bureau voor de Statistiek)
  - Source: https://www.cbs.nl/-/media/cbs/onze-diensten/methoden/classificaties/overig/gemeenten-alfabetisch-2026.xlsx
  - Converted from XLSX to CSV → `data/municipalities.csv`

- **Municipalities GeoJSON** — provided by HR
  - Geospatial boundaries for Dutch municipalities → `data/municipalities_nl.geojson`

---

## Prerequisites

- Docker & Docker Compose
- Git

---

## Getting Started

### 1. Build and Start Services

```bash
docker compose build --no-cache
docker compose up
```

This starts:
- **web** — Django application
- **db** — PostgreSQL + PostGIS

### 2. Run Migrations 
###### Migrations run by default (for the sake of simplicity) with the ```docker compose up``` command. You can also run it manually 
```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

### 3. Create a Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

> NOTE: A default superuser is created automatically on startup — **username:** `rootuser`, **password:** `rootpassword`. You can use this directly or create your own with the command above.

### 4. Load Municipality Data

Populate the database with the Netherlands municipalities dataset:

```bash
docker compose exec web python scripts/upload_data.py --username=rootuser --password=rootpassword
```

> Replace `rootuser` / `rootpassword` with your own credentials if you created a custom superuser.

### 5. Access the Application

| Service | URL |
|---|---|
| Admin Panel | http://localhost:8005/admin/ |
| API Base | http://localhost:8005/api/ |
| Browsable API | http://localhost:8005/api/municipalities/ |

---

## Authentication

The API uses **JWT (JSON Web Token)** authentication (5-minute access token, 1-day refresh token).

> NOTE: Before using any endpoint, log in via the admin panel at `http://localhost:8005/admin/` to establish a session, or obtain a JWT token as described below.

### Get Access Token

```bash
curl -X POST http://localhost:8005/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### Refresh Token

```bash
curl -X POST http://localhost:8005/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token"}'
```

---

## API Endpoints

All endpoints require `Authorization: Bearer <access_token>`.

### List All Municipalities

```
GET /api/municipalities/
```

**Response `200 OK`:**
```json
{
  "next": "http://localhost:8005/api/municipalities/?page=2",
  "prev": null,
  "results": [
    {
      "id": 1,
      "name": "Amsterdam",
      "code": "GM0363",
      "geom": { "type": "MultiPolygon", "coordinates": ["..."] }
    }
  ]
}
```

---

### Create a Municipality

```
POST /api/municipalities/
```

**Request body:**
```json
{
  "name": "Test Municipality",
  "code": "TEST1",
  "geom": {
    "type": "MultiPolygon",
    "coordinates": [[[[6.8638226363766535, 52.22593356417747],
                      [6.8638226363766535, 52.22336306334935],
                      [6.867694876080947,  52.22336306334935],
                      [6.867694876080947,  52.22593356417747],
                      [6.8638226363766535, 52.22593356417747]]]]
  }
}
```

**Response `201 Created`:**
```json
{
  "success": "New municipality created with name 'Test Municipality', code: 'TEST1' and id 345"
}
```

**Edge cases:**

| Scenario | Status | Response |
|---|---|---|
| Missing `name` or `code` | `400` | `{"detail": "Both 'name' and 'code' are required."}` |
| `code` already exists | `400` | `{"detail": "Municipality with code 'TEST1' already exists."}` |

---

### Update a Municipality (Partial)

```
PATCH /api/municipalities/{id}/
```

**Request body** (all fields optional):
```json
{
  "name": "Updated Municipality",
  "code": "NL-NEW-001",
  "geom": null
}
```

**Response `200 OK`:**
```json
{
  "success": "Municipality updated to name 'Updated Municipality', code 'NL-NEW-001'"
}
```

**Edge cases:**

| Scenario | Status | Response |
|---|---|---|
| `id` not found | `404` | `{"detail": "No Municipalities matches the given query."}` |
| `code` already used by another municipality | `400` | `{"detail": "Municipality with code 'NL-NEW-001' already exists."}` |

---

### Delete a Municipality

```
DELETE /api/municipalities/{id}/
```

**Response `204 No Content`** on success.

**Edge cases:**

| Scenario | Status | Response |
|---|---|---|
| `id` not found | `404` | `{"detail": "No Municipalities matches the given query."}` |

---

### Filter by Bounding Box

Query municipalities intersecting a geographic area (`min_lng,min_lat,max_lng,max_lat`):

```
GET /api/municipalities/bbox_filter/?in_bbox=5.855075164747461,52.84452676586113,7.54824215650271,53.48934042770347
```

> Example covers Eelde and surrounding municipalities in Drenthe/Groningen.

**Response `200 OK`** — same paginated format as List. Returns an empty `results` array if no municipalities intersect the given bbox.

---

## Testing the API

### Browser (Browsable API)

1. Log in at `http://localhost:8005/admin/`
2. Visit `http://localhost:8005/api/municipalities/`
3. Use the browsable API interface

### Postman / cURL

**Get token:**
```bash
curl -X POST http://localhost:8005/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**Use token:**
```bash
curl -X GET http://localhost:8005/api/municipalities/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Refresh token:**
```bash
curl -X POST http://localhost:8005/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

---

## Project Structure

```
aiInfraTask/
├── settings.py
├── urls.py
├── wsgi.py / asgi.py
└── quickstart/
    ├── models.py
    ├── views.py
    ├── seriallizers.py
    └── migrations/
```


---

## References

- [DRF Quickstart](https://www.django-rest-framework.org/tutorial/quickstart/)
- [DRF ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#installation)
- [JWT Auth with Django](https://www.geeksforgeeks.org/python/jwt-authentication-with-django-rest-framework/)
- [GeoDjango Docs](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/)