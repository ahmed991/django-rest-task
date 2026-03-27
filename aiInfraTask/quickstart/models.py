# from django.db import models
from django.contrib.gis.db import models

# Municipality Model Definition
class Municipalities(models.Model):
    id  = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, default="")
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.name
    