from django.urls import include, path
from rest_framework import routers

from aiInfraTask.quickstart import views

# Registering municipalities viewSet
router = routers.DefaultRouter()
router.register(r"municipalities", views.MunicipalityViewSet)

urlpatterns = [
    path('', include(router.urls))
]