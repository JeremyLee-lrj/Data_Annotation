from django.urls import path

from . import views

urlpatterns = [
    path('get-current', views.get_current),
    path('list', views.List),
    path('login', views.Login),
    path('logout', views.Logout),
    path('register', views.Register),
    path('register-manager', views.Register_Manager),
]
