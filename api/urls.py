from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from . import views

router = routers.DefaultRouter()


router.register(r'sensor_data', views.SensorDataViewSet)

urlpatterns = [
    path('docs/', include_docs_urls(title='API Docs')),
    path('', include(router.urls)),
]
