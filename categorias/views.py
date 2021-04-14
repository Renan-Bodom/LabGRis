from django.shortcuts import render
from LabGRis.decorators import validate_session, getSessionUser
from LabGRis.funcoesCompartilhadas import criarListaDoBanco, criarListaDoBancoKEY
from LabGRis.pyrebase_settings import db
import datetime


@validate_session
def categorias(request):
    data = {}           # Dicionário DJango
    data['SessionUser'] = getSessionUser(request)
    data['context']     = ""

    data['datenow'] = datetime.datetime.now()

    # Bancos
    bancoCategoria = "categoria"

    # Redirecionamento de páginas
    redirectCat = 'url_categoria'


    #########  Busca categoria já cadastradas
    categoriaSalvas = db.child(bancoCategoria).get()
    listaCategoria  = criarListaDoBanco(categoriaSalvas)
    data['listaCategoria'] = listaCategoria



    return render(request, 'categorias/categorias.html', data)


@validate_session
def novaCategoria(request):
    data = {}  # Dicionário DJango

    # Bancos
    bancoCategoria = "categoria"

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    return render(request,'categorias/manipularCategoria.html', data)