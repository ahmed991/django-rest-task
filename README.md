
## django rest framework task

### Author: Ahmed Hanif

This is a Django REST Framework API for managing municipal boundaries in the Netherlands with geospatial capabilities. The project uses PostgreSQL with PostGIS for storing and querying geographic data.

---

## Data Sources

- **Municipalities CSV**: CBS (Centraal Bureau voor de Statistiek)
  - Source: https://www.cbs.nl/-/media/cbs/onze-diensten/methoden/classificaties/overig/gemeenten-alfabetisch-2026.xlsx
  - Converted from XLSX to CSV format
  - Location: `data/municipalities.csv`

- **Municipalities GeoJSON**: provided by HR
  - Geospatial boundaries for Dutch municipalities
  - Location: `data/municipalities_nl.geojson`

---

## Deliverables

[DONE] **CRUD REST API for GeoJSON Features**
- Create, Read, Update, Delete operations on GeoJSON feature objects
- Paginated results (100 features per page)
- Format: `{"next": "...", "prev": "...", "results": [...]}`

[DONE] **Bounding Box Filtering**
- Filter features by geographic bounding box
- Query municipalities that intersect with a specified area
- Endpoint: `/api/municipalities/bbox_filter/?in_bbox=min_lng,min_lat,max_lng,max_lat`

[DONE] **Dataset Integration**
- Loaded Netherlands municipalities GeoJSON dataset
- Data persisted in PostgreSQL with PostGIS extension

[DONE] **Docker Containerization** (Bonus)
- Dockerfile for Django application
- docker-compose.yml with web service and PostGIS database
- Easy setup and deployment

[DONE] **JSON Web Token Authentication** (Bonus)
- JWT-based authorization for API endpoints
- Token refresh mechanism
- 5-minute token lifetime with 1-day refresh token lifetime

---

---

## Prerequisites

- docker & docker compose installed on your system
- git (for cloning the repository)

---

## Getting Started with Docker

### 1. Build and Start Services

Start the Docker containers:

```bash
docker compose build
docker compose up
```

This will start:
- **web** service: Django application
- **db** service: PostgreSQL database with PostGIS

### 2. Run Database Migrations

Apply all database migrations to set up the schema:

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### 3. Create a Superuser (Optional)

Create an admin account to access the Django admin panel:

```bash
docker-compose exec web python manage.py createsuperuser
```

### 4. Access the Application

- **API Base URL**: `http://localhost:8005/api/`
- **Admin Panel**: `http://localhost:8005/admin/`
- **Browsable API**: `http://localhost:8005/api/municipalities/`

---

## Authentication

This API uses **JWT (JSON Web Token)** authentication.

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

## Testing the API

### Method 1: Browser (Browsable API)

1. Login to admin panel: `http://localhost:8005/admin/`
2. Visit: `http://localhost:8005/api/municipalities/`
3. Use the browsable API interface to test endpoints

**Test Create Geometry:**
```json
{
  "name": "Test Municipality",
  "code": "TEST1",
  "geom": {
    "type": "MultiPolygon",
    "coordinates": [
      [
        [
          [6.8638226363766535, 52.22593356417747],
          [6.8638226363766535, 52.22336306334935],
          [6.867694876080947, 52.22336306334935],
          [6.867694876080947, 52.22593356417747],
          [6.8638226363766535, 52.22593356417747]
        ]
      ]
    ]
  }
}
```

**Test Update:**
```json
{
  "name": "Updated Municipality",
  "code": "NL-NEW-001",
  "geom": null
}
```

**Test Bounding Box Filter:**
Navigate to: `http://localhost:8005/api/municipalities/bbox_filter/?in_bbox=4.636879905143701,52.18962248356709,5.30002510140082,52.44034985332962`

---

### Method 2: Postman / cURL

**Get Access Token:**
```bash
curl -X POST http://localhost:8005/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**Use Token in Requests:**
```bash
curl -X GET http://localhost:8005/api/municipalities/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Refresh Token (expires in 5 min):**
```bash
curl -X POST http://localhost:8005/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

---

## API Endpoints

### List All Municipalities

```bash
GET /api/municipalities/
Authorization: Bearer <access_token>
```

### Create a Municipality

```bash
POST /api/municipalities/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Test Municipality",
  "code": "TEST1",
  "geom": {
    "type": "MultiPolygon",
    "coordinates": [
      [
        [
          [6.8638226363766535, 52.22593356417747],
          [6.8638226363766535, 52.22336306334935],
          [6.867694876080947, 52.22336306334935],
          [6.867694876080947, 52.22593356417747],
          [6.8638226363766535, 52.22593356417747]
        ]
      ]
    ]
  }
}
```

### Update a Municipality (Partial)

```bash
PATCH /api/municipalities/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Updated Municipality",
  "code": "NL-NEW-001",
  "geom": null
}
```

### Filter Municipalities by Bounding Box

Query municipalities that intersect with a geographic bounding box (min_lng, min_lat, max_lng, max_lat):

```bash
GET /api/municipalities/bbox_filter/?in_bbox=4.636879905143701,52.18962248356709,5.30002510140082,52.44034985332962
Authorization: Bearer <access_token>
```

---

## Project Structure

```
aiInfraTask/                    # Django Project
├── settings.py               # Configuration
├── urls.py                   # Root URL routing
├── wsgi.py / asgi.py        # Server entry points
└── quickstart/               # Main App
    ├── models.py            # Municipalities model
    ├── views.py             # API ViewSets
    ├── seriallizers.py      # Data serializers
    └── migrations/          # Database migrations
```

---

## Useful Docker Commands

### View Running Containers
```bash
docker-compose ps
```

### View Application Logs
```bash
docker-compose logs -f web
```

### Stop All Services
```bash
docker-compose down
```

### Remove All Services and Data
```bash
docker-compose down -v
```

### Access Django Shell
```bash
docker-compose exec web python manage.py shell
```

---

## References

- [Django REST Framework - Quickstart](https://www.django-rest-framework.org/tutorial/quickstart/)
- [Django REST Framework - ViewSets (custom routes)](https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing)
- [Django REST Framework SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#installation)
- [JWT Authentication with Django](https://www.geeksforgeeks.org/python/jwt-authentication-with-django-rest-framework/)
- [Django GIS/GeoDjango Documentation](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/)