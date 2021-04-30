from django.urls import path
from . import views

urlpatterns = [
    path('', views.categorias),
    path('novaCategoria/', views.novaCategoria),
    path('alterarCategoria/<categoria>', views.alterarCategoria),
    path('excluirCategoria/<categoria>', views.excluirCategoria)
]