"""LabGRis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('responderFicha.urls'), name='url_main'),
    path('usuario/', include('users.urls'), name='url_users'),
    path('perguntas/', include('perguntas.urls'), name='url_perguntas'),
    path('categorias/', include('categorias.urls'), name='url_categorias'),
    path('modeloFichas/', include('modeloFichas.urls'), name='url_modeloFichas'),
    path('fichas/', include('responderFicha.urls'), name='url_responderFicha')
]
