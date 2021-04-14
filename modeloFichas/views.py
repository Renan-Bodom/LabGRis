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

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    return render(request, "modeloFichas/manipularModeloFicha.html", data)