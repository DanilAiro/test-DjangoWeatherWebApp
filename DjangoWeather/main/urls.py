from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path('get_city_suggestions/', views.get_city_suggestions, name='get_city_suggestions'),
]