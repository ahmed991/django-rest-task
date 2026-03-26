docker compose run web python manage.py makemigrations
docker compose run web python manage.py migrate


https://www.geeksforgeeks.org/python/jwt-authentication-with-django-rest-framework/


https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#installation


http://localhost:8000/get/?in_bbox=4.636879905143701,%2052.18962248356709,%205.30002510140082,%2052.44034985332962




test create geometry

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