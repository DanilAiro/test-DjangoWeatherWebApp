from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path('get_city_suggestions/', views.get_city_suggestions, name='get_city_suggestions'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
