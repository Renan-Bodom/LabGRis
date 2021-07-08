from django.shortcuts import render, redirect
from LabGRis.decorators import validate_session, getSessionUser
from LabGRis.funcoesCompartilhadas import criarListaDoBanco, criarListaDoBancoKEY
from LabGRis.pyrebase_settings import db
import datetime
from perguntas.classes.Perguntas import Pergunta
from categorias.classes.Categorias import Categoria
from modeloFichas.classes.ModeloFicha import Ficha

# Bancos
tabelaBanco = "Templates de Fichas"
tabelaUsers = "users"

# Redirects
redirectModeloFicha = '/modeloFichas/'

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
    data['datenow'] = [datetime.datetime.now().strftime('%d/%m/%Y'), datetime.datetime.now().strftime('%H:%M:%S')]

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


    if request.method == "POST":
        formIdUsuario = request.POST.get('idUsuario', '')
        formDataAlterado = request.POST.get('dataAlterado', '')
        formNomeModelo = request.POST.get('nomeModelo', '')
        formSelCategoria = request.POST.getlist('dualListBox', '')

        listaObjectCategoria = []
        for cat in formSelCategoria:
            listaObjectPergunta = []
            categoriaBanco = db.child("categoria").child(cat).child("tituloPerguntas").get()
            dadosCategoria = criarListaDoBanco(categoriaBanco)

            for perg in dadosCategoria:
                if perg['fechada'] == True:  # Checando se a pergunta é fechada
                    objectPergunta = Pergunta(perg["tituloPergunta"], perg["alternativas"])
                    listaObjectPergunta.append(objectPergunta)
                else:
                    objectPergunta = Pergunta(perg["tituloPergunta"], 'dissertativa')
                    listaObjectPergunta.append(objectPergunta)
                    #print(objectPergunta.get_tituloPergunta(), objectPergunta.get_tituloAlternativa())

            idCateogira = 1  #########################################################Precisa arrumar!!
            objectCategoria = Categoria(cat, idCateogira, listaObjectPergunta)
            listaObjectCategoria.append(objectCategoria)

        objectModeloFicha = Ficha(formNomeModelo, formIdUsuario, listaObjectCategoria)

        # Criando o nó do modelo de ficha
        db.child(tabelaBanco).child(formNomeModelo).set(objectModeloFicha.enviarFichaFirebase())

        contCat = 0
        for lCat in objectModeloFicha.get_objectCategorias():
            db.child(tabelaBanco).child(formNomeModelo).update(objectModeloFicha.updateFichaCategoriaFirebase(lCat.get_tituloCategoria(), lCat.get_idCategoria(), contCat))
            contPG = 0
            for pg in lCat.get_objectPerguntas():
                infoPergunta = db.child("categoria").child(lCat.get_tituloCategoria()).child("tituloPerguntas").child(
                    pg.get_tituloPergunta()).get().val()                        # Recupera informações da pergunta

                if infoPergunta['fechada'] == True:
                    if infoPergunta['multiplasRespostas'] == True:
                        db.child(tabelaBanco).child(formNomeModelo).child("categorias").child(contCat).child("perguntas").child(contPG).update(pg.enviarModeloPerguntaMultiplasRespostasFirebase(pg.get_tituloAlternativa()))
                    else:
                        db.child(tabelaBanco).child(formNomeModelo).child("categorias").child(contCat).child("perguntas").child(contPG).update(pg.enviarModeloPerguntaFirebase(pg.get_tituloAlternativa()))
                else:
                    db.child(tabelaBanco).child(formNomeModelo).child("categorias").child(contCat).child("perguntas").child(contPG).update(pg.enviarModeloPerguntaDissertativaFirebase())

                contPG = contPG + 1
            contCat = contCat + 1

        return redirect(redirectModeloFicha)


    return render(request, "modeloFichas/manipularModeloFicha.html", data)


def alterarModeloFicha(request, modFichaAlterar):
    data = {}  # Dicionário DJango
    data['datenow'] = [datetime.datetime.now().strftime('%d/%m/%Y'), datetime.datetime.now().strftime('%H:%M:%S')]

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    data['teste'] = "Teste"

    return render(request, 'modeloFichas/alterarModeloFicha.html', data)

def excluirModeloFicha(request, modFichaExcluir):
    db.child(tabelaBanco).child(modFichaExcluir).remove()

    return redirect('/modeloFichas/')