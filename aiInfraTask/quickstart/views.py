from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import GEOSGeometry
from aiInfraTask.quickstart.seriallizers import GroupSerializer, UserSerializer, MunicipalitiesSerializer
from .models import Municipalities
from django.shortcuts import render
from django.contrib.gis.geos import Polygon
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    authentication_classes = [JWTAuthentication]

    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class MunicipalityViewSet(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = MunicipalitiesSerializer
    queryset = Municipalities.objects.all()

    def get_queryset(self):
        queryset = self.queryset

        bbox = self.request.query_params.get('in_bbox', None)

        if(bbox):
            min_lng, min_lat, max_lng, max_lat = map(float, bbox.split(','))
            bbox_geom = Polygon.from_bbox((min_lng, min_lat, max_lng, max_lat))
            bbox_geom.srid = 4326


            # bbox_geom = GEOSGeometry(
            #     f'POLYGON(({min_lng} {min_lat}, {max_lng} {min_lat}, {max_lng} {max_lat},{min_lng} {max_lat}, {min_lng} {min_lat}))',
            #     srid=4326
            # )
            print(bbox_geom)

            queryset = queryset.filter(geom__intersects=bbox_geom)
        
        return queryset
    
    def create(self, request, *args, **kwargs):

        name = request.data.get('name')
        code = request.data.get('code')
        geometry = request.data.get('geom')

        if not name or not code:
            return Response(
                {"detail": "Both 'name' and 'code' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Municipalities.objects.filter(code=code).exists():
            return Response(
                {"detail": f"Municipality with code '{code}' already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"success": f"New municipality created with name '{name}', code: '{code}'"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()




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