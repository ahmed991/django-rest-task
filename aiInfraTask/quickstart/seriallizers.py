from django.contrib.auth.models import Group, User
from .models import Municipalities
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]

class MunicipalitiesSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Municipalities
        fields = ["id", "name", "code"]
        geo_field = 'geom'