from django.shortcuts import render, redirect
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

    # Bancos
    bancoPergunta = "perguntas"

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    # OPÇÃO dissertativa
    # if request.method == 'POST':
    if request.method == "POST" and "formPerguntasDissertativa" in request.POST:
        enunciado = 'enunciado'
        formEnunciado = request.POST.get(enunciado, 'Enunciado não carregado')

        print("Dissertativa selecionadas", formEnunciado)
        #objectPergunta = Pergunta(formEnunciado, alternativa="dissertativa")
        #db.child(bancoPergunta).child(formEnunciado).set(objectPergunta.enviarPerguntaDissertativaFirebase())

        return redirect('/perguntas/')

    # OPÇÃO alternativas
    if request.method == "POST" and "formPerguntas" in request.POST:
        enunciado = 'enunciado'
        formEnunciado = request.POST.get(enunciado, 'Enunciado não carregado')
        alternativasSel = 'alternativas'
        formAlternativas = request.POST.getlist(alternativasSel, 'Alternativas não carregada')

        print("Alternativas selecionadas", formEnunciado, formAlternativas)
        #objectPergunta = Pergunta(formEnunciado, formAlternativas)
        #db.child(bancoPergunta).child(formEnunciado).set(objectPergunta.enviarPerguntaFirebase(formAlternativas))

        return redirect('/perguntas/')

    return render(request,'perguntas/manipularPerguntas.html', data)