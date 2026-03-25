from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, generics
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import GEOSGeometry
from aiInfraTask.quickstart.seriallizers import GroupSerializer, UserSerializer, MunicipalitiesSerializer
from .models import Municipalities
from django.shortcuts import render
from django.contrib.gis.geos import Polygon





class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



class MunicipalitiesList(generics.ListCreateAPIView):
    serializer_class = MunicipalitiesSerializer



    def get_queryset(self):
        queryset = Municipalities.objects.all()

        bbox = self.request.query_params.get('in_bbox', None)

        if(bbox):
            min_lng, min_lat, max_lng, max_lat = map(float, bbox.split(','))
            bbox_geom = Polygon.from_bbox((min_lng, min_lat, max_lng, max_lat))


            # bbox_geom = GEOSGeometry(
            #     f'POLYGON(({min_lng} {min_lat}, {max_lng} {min_lat}, {max_lng} {max_lat},{min_lng} {max_lat}, {min_lng} {min_lat}))',
            #     srid=4326
            # )
            print(bbox_geom)

            queryset = queryset.filter(geom__intersects=bbox_geom)
        
        return queryset

    
    # queryset = Municipalities.objects.all()
    # serializer_class = MunicipalitiesSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# class MunicipalitiesCreate(generics.CreateAPIView):
#     queryset = Municipalities.objects.all()
#     serializer_class = MunicipalitiesSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# class MunicipalitiesDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Municipalities.objects.all()
#     serializer_class = MunicipalitiesSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# class MunicipalitiesUpdate(generics.UpdateAPIView):
#     queryset = Municipalities.objects.all()
#     serializer_class = MunicipalitiesSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# class 