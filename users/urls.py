from django.urls import path
from . import views

urlpatterns = [
    path('', views.users),
    path('entrar/', views.login),
    path('validar_acesso/', views.valida_senha),
    path('sair/', views.sair),
    path('listar/', views.listaUsers),
    path('novoUsuario/', views.novoUsuario),
    path('listar/alterarUsuario/<userAlterar>', views.alterarUsuario),
    path('listar/removerUsuario/<userRemover>', views.removerUsuario),
    path('esquecisenha/', views.esqueciSenha)
]