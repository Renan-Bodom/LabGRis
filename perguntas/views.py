from django.shortcuts import render
from LabGRis.decorators import validate_session, getSessionUser
import datetime
from LabGRis.pyrebase_settings import db, auth

@validate_session
def perguntas(request):
    data = {}   # Dicionário DJango

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context']     = ""

    data['datenow'] = datetime.datetime.now()

    # Bancos
    bancoPergunta = "perguntas"

    # Redirecionamento de páginas
    redirectPergunta = 'url_perguntas'


    #########  Recupera perguntas já cadastradas
    perguntasSalvas = db.child(bancoPergunta).get()
    listaPerguntas = []
    for per in perguntasSalvas.each():
        listaPerguntas.append(per.val())
    data['listaPerguntas'] = listaPerguntas



    return render(request,'perguntas/perguntas.html', data)


def novaPergunta(request):
    data = {}  # Dicionário DJango

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    return render(request,'perguntas/manipularPerguntas.html', data)