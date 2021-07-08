from django.shortcuts import render, redirect
from LabGRis.decorators import validate_session, getSessionUser
from LabGRis.funcoesCompartilhadas import criarListaDoBanco, criarListaDoBancoKEY
from LabGRis.pyrebase_settings import db
import datetime
from perguntas.classes.Perguntas import Pergunta
from .classes.Categorias import Categoria

# Bancos
bancoCategoria = "categoria"
bancoPerguntas = "perguntas"

# Redirecionamento de páginas
redirectCat = '/categorias/'


@validate_session
def categorias(request):
    data = {}           # Dicionário DJango
    data['SessionUser'] = getSessionUser(request)
    data['context']     = ""

    data['datenow'] = datetime.datetime.now()

    #########  Busca categoria já cadastradas
    categoriaSalvas = db.child(bancoCategoria).get()
    listaCategoria  = criarListaDoBanco(categoriaSalvas)
    data['listaCategoria'] = listaCategoria



    return render(request, 'categorias/categorias.html', data)


@validate_session
def novaCategoria(request):
    data = {}  # Dicionário DJango

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    #########  Busca perguntas para listar no dualList
    perguntasSalvas = db.child("perguntas").get()
    listaPerguntas = criarListaDoBanco(perguntasSalvas)

    apenasPerguntas = []
    for perguntas in listaPerguntas:
        apenasPerguntas.append(perguntas['tituloPergunta'])

    data['listaPerguntas'] = apenasPerguntas


    ###### Identifica o botão salvar
    if request.method == "POST":

        ###### Capta informações do form
        formNomeCategoria = request.POST.get('nomeCategoria', '')
        formSelPerguntas = request.POST.getlist('dualListBox', '')
        formIdCategoriaMae = '123'

        listaObjectPerguntas = []
        for per in formSelPerguntas:
            perguntasDoBanco = db.child(bancoPerguntas).child(per).get().val()
            if perguntasDoBanco['fechada'] == True:
                objectPergunta = Pergunta(perguntasDoBanco['tituloPergunta'], perguntasDoBanco['alternativas'])
            else:
                objectPergunta = Pergunta(perguntasDoBanco['tituloPergunta'], 'dissertativa')
            listaObjectPerguntas.append(objectPergunta)

        objectCategoria = Categoria(formNomeCategoria, formIdCategoriaMae, listaObjectPerguntas)
        listaPerguntas = objectCategoria.get_objectPerguntas()

        # Criando o nó da categoria criada
        db.child(bancoCategoria).child(formNomeCategoria).set(objectCategoria.enviarCategoriaFirebase())
        # Salvando perguntas dessa categoria
        for objPergunta in listaPerguntas:
            infoPergunta = db.child(bancoPerguntas).child(objPergunta.get_tituloPergunta()).get().val()
            if infoPergunta['fechada'] == True:                 # Checando se a pergunta é fechada
                if infoPergunta['multiplasRespostas'] == True:  # Chegando se a pergunta tem mais de uma resposta
                    db.child(bancoCategoria).child(formNomeCategoria).child("tituloPerguntas").child(
                        objPergunta.get_tituloPergunta()).update(
                        objPergunta.enviarPerguntaMultiplasRespostasFirebase(objPergunta.get_tituloAlternativa()))
                else:
                    db.child(bancoCategoria).child(formNomeCategoria).child("tituloPerguntas").child(
                        objPergunta.get_tituloPergunta()).update(
                        objPergunta.enviarPerguntaFirebase(objPergunta.get_tituloAlternativa()))
            else:
                db.child(bancoCategoria).child(formNomeCategoria).child("tituloPerguntas").child(
                    objPergunta.get_tituloPergunta()).update(
                    objPergunta.enviarPerguntaDissertativaFirebase())

        return redirect(redirectCat)

    return render(request,'categorias/manipularCategoria.html', data)


def alterarCategoria(request, categoria):
    data = {}  # Dicionário DJango

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    # Informações da categoria
    dadosCategoria = db.child(bancoCategoria).child(categoria).get().val()

    #########  Busca perguntas para listar no dualList
    perguntasSalvas = db.child("perguntas").get()
    apenasPerguntas = []
    # Monta lista de perguntas
    for perguntas in perguntasSalvas:
        apenasPerguntas.append(perguntas.val()['tituloPergunta'])
    # Remove as já selecionadas
    for pergCategoria in dadosCategoria['tituloPerguntas']:
        apenasPerguntas.remove(pergCategoria)
    data['listaPerguntas'] = apenasPerguntas

    # Informações da categoria para alterar
    data['dadosCategoria'] = dadosCategoria

    return render(request,'categorias/alterarCategoria.html', data)

def excluirCategoria(request, categoria):
    db.child(bancoCategoria).child(categoria).remove()

    return redirect(redirectCat)