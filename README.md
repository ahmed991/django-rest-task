# Django REST Framework Task

**Author:** Ahmed Hanif

## Run

```bash
git clone https://github.com/ahmed991/django-rest-task.git
cd django-rest-task
```

```bash
# Linux/Mac
cp .env.example .env

# Windows
copy .env.example .env
```

```bash
docker compose build --no-cache
docker compose up
```

> Migrations run automatically on startup. To run manually:
> ```bash
> docker compose exec web python manage.py makemigrations
> docker compose exec web python manage.py migrate
> ```

## Load Data into the Municipalities database

```bash
#In another terminal within the same directory 

docker compose exec web python scripts/upload_data.py --username=rootuser --password=rootpassword
```

> Default credentials — **username:** `rootuser`, **password:** `rootpassword`.
> To create your own: `docker compose exec web python manage.py createsuperuser`

## Access

| Service | URL |
|---|---|
| Admin Panel | http://localhost:8005/admin/ |
| API | http://localhost:8005/api/ |

> Before calling any endpoint, log in at `http://localhost:8005/admin/` or get a JWT token:

```bash
curl -X POST http://localhost:8005/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "rootuser", "password": "rootpassword"}'
```

Use the token as `Authorization: Bearer <access_token>` on all requests.

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/municipalities/` | List all (paginated, 100/page) |
| `POST` | `/api/municipalities/` | Create |
| `PATCH` | `/api/municipalities/{id}/` | Partial update |
| `DELETE` | `/api/municipalities/{id}/` | Delete |
| `GET` | `/api/municipalities/bbox_filter/?in_bbox=min_lng,min_lat,max_lng,max_lat` | Filter by bounding box |

For full request/response details and edge cases see [DETAILED_README.md](UPDATED_README.md).
