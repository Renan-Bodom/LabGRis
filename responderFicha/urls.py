from django.urls import path
from . import views

urlpatterns = [
    path('', views.responderFicha),
    path('modelosFicha/', views.modelosFicha),
    path('preenchendoFicha/<fichaSelec>', views.preenchendoFicha)
]