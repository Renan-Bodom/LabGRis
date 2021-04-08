from django.shortcuts import render
from LabGRis.decorators import validate_session, getSessionUser
from LabGRis.funcoesCompartilhadas import criarListaDoBanco, criarListaDoBancoKEY
from LabGRis.pyrebase_settings import db


@validate_session
def responderFicha(request):
    data = {}
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    # Bancos
    bancoModeloFicha = "Templates de Fichas"

    #########  Busca Modelos de Ficha já cadastradas
    fichaSalvas = db.child(bancoModeloFicha).get()
    listaFicha = criarListaDoBanco(fichaSalvas)
    data['listaFicha'] = listaFicha

    return render(request, 'responderFicha/responderFicha.html', data)