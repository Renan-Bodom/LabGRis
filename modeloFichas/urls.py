from django.urls import path
from . import views

urlpatterns = [
    path('', views.modeloFichas),
    path('novoModeloFicha/', views.novoModeloFicha),
    path('excluir/<modFichaExcluir>', views.excluirModeloFicha)
]