from django.urls import path

from . import views

urlpatterns = [
    path('list', views.List),
    path('label', views.label),
]
