# from django.db import models
from django.contrib.gis.db import models

# Create your models here.
class Municipalities(models.Model):
    id  = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    geom = models.MultiPolygonField()

    def __str__(self):
        return self.name