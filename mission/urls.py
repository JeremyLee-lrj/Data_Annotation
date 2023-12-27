from django.urls import path

from . import views

urlpatterns = [
    path('list', views.List),
    path('list-by-dataset', views.list_by_dataset),
    path('assign', views.assign),
    path('reassign', views.reassign),
]
