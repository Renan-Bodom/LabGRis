from django.urls import path
from . import views

urlpatterns = [
    path('', views.perguntas),
    path('novaPergunta/', views.novaPergunta),
    path('excluirPergunta/<pergunta>', views.excluirPergunta),
    path('alterarPergunta/<pergunta>', views.alterarPergunta)
]