from django.shortcuts import render
from LabGRis.decorators import validate_session, getSessionUser
from LabGRis.funcoesCompartilhadas import criarListaDoBanco, criarListaDoBancoKEY
from LabGRis.pyrebase_settings import db


@validate_session
def modeloFichas(request):
    data = {}
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    # Bancos
    tabelaBanco = "Templates de Fichas"

    #########  Busca fichas já cadastradas
    fichaSalvas = db.child(tabelaBanco).get()
    listaFicha = criarListaDoBanco(fichaSalvas)
    data['listaFicha'] = listaFicha

    return render(request, 'modeloFichas/modeloFichas.html', data)

@validate_session
def novoModeloFicha (request):
    data = {}  # Dicionário DJango

    # Bancos
    tabelaBanco = "Templates de Fichas"
    tabelaUsers = "users"

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    #########  Busca usuarios
    usuariosSalvos = db.child(tabelaUsers).get()
    listaUsuarios = criarListaDoBanco(usuariosSalvos)
    data['listaUsuarios'] = listaUsuarios

    #########  Busca categoria já categoria
    categoriaSalvas = db.child("categoria").get()
    listaCategoria = criarListaDoBanco(categoriaSalvas)
    apenasNomeCategoria = []
    for listCat in listaCategoria:
        apenasNomeCategoria.append(listCat['nome'])
    data['listaCategoria'] = apenasNomeCategoria

    return render(request, "modeloFichas/manipularModeloFicha.html", data)