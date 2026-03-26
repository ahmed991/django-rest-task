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
from rest_framework.decorators import action


class MunicipalityViewSet(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MunicipalitiesSerializer
    queryset = Municipalities.objects.all()



    # BBOX filter endpoint

    @action(detail=False, methods=['get'])    
    def bbox_filter(self, request):
        queryset = self.queryset
        bbox = request.query_params.get('in_bbox', None)
        if(bbox):
            min_lng, min_lat, max_lng, max_lat = map(float, bbox.split(','))
            bbox_geom = Polygon.from_bbox((min_lng, min_lat, max_lng, max_lat))
            bbox_geom.srid = 4326
            print(bbox_geom)

            queryset = queryset.filter(geom__intersects=bbox_geom)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    # Create endpoint with name and code checks to keep municipalities unique

    def create(self, request, *args, **kwargs):

        name = request.data.get('name')
        code = request.data.get('code')

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
    
    # Partial update override, to control de duplication of the code
    
    def partial_update(self, request, *args, **kwargs):
        selected_feature = self.get_object()

        new_name = request.data.get('name', selected_feature.name)
        new_code = request.data.get('code', selected_feature.code)


        if Municipalities.objects.exclude(id=selected_feature.id).filter(code=new_code).exists():
            return Response(
                {"detail": f"Municipality with code '{new_code}' already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(selected_feature, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)        
        self.perform_update(serializer)
        return Response(
            {"success": f"Municipality updated to name '{new_name}', code '{new_code}'"},
            status=status.HTTP_200_OK
        )

