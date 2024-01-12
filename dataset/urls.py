from django.urls import path

from . import views

urlpatterns = [
    path('get', views.get_dataset),
    path('list', views.list_dataset),
    path('upload', views.upload_dataset),
    path('download', views.download_dataset),
]
