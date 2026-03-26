from django.urls import include, path
from django.contrib import admin
from django.views.generic import RedirectView


from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from aiInfraTask.quickstart import views

router = routers.DefaultRouter()
# router.register(r"users", views.UserViewSet)
# router.register(r"groups", views.GroupViewSet)
router.register(r"municipalities", views.MunicipalityViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url = '/api'),name="Home page"),


]