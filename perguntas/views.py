from django.shortcuts import render, redirect
from LabGRis.decorators import validate_session, getSessionUser
import datetime
from LabGRis.pyrebase_settings import db, auth
from perguntas.classes.Perguntas import Pergunta
from LabGRis.funcoesCompartilhadas import criarListaDoBanco


# Bancos
bancoPergunta = "perguntas"

# Redirect
pagPerguntas = '/perguntas/'

@validate_session
def perguntas(request):
    data = {}   # Dicionário DJango

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context']     = ""

    data['datenow'] = datetime.datetime.now()


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

    # OPÇÃO dissertativa
    # if request.method == 'POST':
    if request.method == "POST" and "formPerguntasDissertativa" in request.POST:
        enunciado = 'enunciado'
        formEnunciado = request.POST.get(enunciado, 'Enunciado não carregado')

        objectPergunta = Pergunta(formEnunciado, alternativa="dissertativa")
        db.child(bancoPergunta).child(formEnunciado).set(objectPergunta.enviarPerguntaDissertativaFirebase())

        return redirect(pagPerguntas)

    # OPÇÃO alternativas
    if request.method == "POST" and "formPergunta" in request.POST:
        enunciado = 'enunciado'
        formEnunciado = request.POST.get(enunciado, 'Enunciado não carregado')
        alternativasSel = 'alternativas'
        formAlternativas = request.POST.getlist(alternativasSel, 'Alternativas não carregada')

        objectPergunta = Pergunta(formEnunciado, formAlternativas)
        db.child(bancoPergunta).child(formEnunciado).set(objectPergunta.enviarPerguntaFirebase(formAlternativas))

        return redirect(pagPerguntas)

    # OPÇÃO alternativas
    if request.method == "POST" and "formPerguntaMultiplasRespostas" in request.POST:
        enunciado = 'enunciado'
        formEnunciado = request.POST.get(enunciado, 'Enunciado não carregado')
        alternativasSel = 'alternativas'
        formAlternativas = request.POST.getlist(alternativasSel, 'Alternativas não carregada')

        objectPergunta = Pergunta(formEnunciado, formAlternativas)
        db.child(bancoPergunta).child(formEnunciado).set(objectPergunta.enviarPerguntaMultiplasRespostasFirebase(formAlternativas))

        return redirect(pagPerguntas)

    return render(request,'perguntas/manipularPerguntas.html', data)


def excluirPergunta(request, pergunta):
    db.child(bancoPergunta).child(pergunta).remove()

    return redirect(pagPerguntas)


def alterarPergunta(request, pergunta):
    data = {}  # Dicionário DJango

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    #################################### Alterar pergunta
    # Carrega pergunta
    data['perguntaSelecionada'] = db.child(bancoPergunta).child(pergunta).get().val()

    # Recebendo alterações
    # OPÇÃO dissertativa
    if request.method == "POST" and "formPerguntasDissertativa" in request.POST:
        objectPergunta = Pergunta(pergunta, alternativa="dissertativa")
        db.child(bancoPergunta).child(pergunta).set(objectPergunta.enviarPerguntaDissertativaFirebase())

        return redirect(pagPerguntas)

    # OPÇÃO alternativas
    if request.method == "POST" and "formPergunta" in request.POST:
        alternativasSel = 'alternativas'
        formAlternativas = request.POST.getlist(alternativasSel, 'Alternativas não carregada')

        objectPergunta = Pergunta(pergunta, formAlternativas)
        db.child(bancoPergunta).child(pergunta).set(objectPergunta.enviarPerguntaFirebase(formAlternativas))

        return redirect(pagPerguntas)

    # OPÇÃO alternativas
    if request.method == "POST" and "formPerguntaMultiplasRespostas" in request.POST:
        alternativasSel = 'alternativas'
        formAlternativas = request.POST.getlist(alternativasSel, 'Alternativas não carregada')

        objectPergunta = Pergunta(pergunta, formAlternativas)
        db.child(bancoPergunta).child(pergunta).set(
            objectPergunta.enviarPerguntaMultiplasRespostasFirebase(formAlternativas))

        return redirect(pagPerguntas)

    return render(request,'perguntas/alterarPerguntas.html', data)
