from django.urls import path, include
from . import views


urlpatterns = [
        path('', views.disk_manager, name='disk_manager'),
        path('', include('django.contrib.auth.urls')),
]
