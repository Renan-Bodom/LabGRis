from django.urls import path
from . import views

urlpatterns = [
    path('', views.categorias),
    path('novaCategoria/', views.novaCategoria)
]