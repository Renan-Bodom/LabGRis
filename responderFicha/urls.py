from django.urls import path
from . import views

urlpatterns = [
    path('', views.responderFicha, name='url_responderFicha'),
    path('modelosFicha/', views.modelosFicha),
    path('preenchendoFicha/<fichaSelec>', views.preenchendoFicha),
    path('alterarFicha/<fichaSelec>', views.alterarFicha),
    path('excluirFicha/<fichaSelec>', views.excluirFicha)
]