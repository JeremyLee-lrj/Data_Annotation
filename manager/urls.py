from django.urls import path

from . import views

urlpatterns = [
    path('information/', views.List_Information),
]