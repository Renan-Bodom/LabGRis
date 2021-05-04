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
            categoriaBanco = db.child("categoria").child(cat).child("tituloPergunta").get()
            dadosCategoria = criarListaDoBanco(categoriaBanco)

            for perg in dadosCategoria:
                objectPergunta = Pergunta(perg["tituloPergunta"], perg["alternativas"])
                listaObjectPergunta.append(objectPergunta)
                #print(objectPergunta.get_tituloPergunta(), objectPergunta.get_tituloAlternativa())

            idCateogira = 1  #########################################################Precisa arrumar!!
            objectCategoria = Categoria(cat, idCateogira, listaObjectPergunta)
            listaObjectCategoria.append(objectCategoria)

        objectModeloFicha = Ficha(formNomeModelo, formIdUsuario, listaObjectCategoria)
        listaCategoria = objectModeloFicha.get_objectCategorias()
        listaPerguntas = listaCategoria[0].get_objectPerguntas()
        perguntaDaLista = listaPerguntas[0].get_tituloPergunta()
        alternativasDaLista = listaPerguntas[0].get_tituloAlternativa()
        #print('AQUI', objectModeloFicha.get_tituloFicha(), listaCategoria[0].get_tituloCategoria(), perguntaDaLista, alternativasDaLista)

        db.child(tabelaBanco).child(formNomeModelo).set(objectModeloFicha.enviarFichaFirebase())

        contCat = 0
        for lCat in listaCategoria:
            db.child(tabelaBanco).child(formNomeModelo).update(objectModeloFicha.updateFichaCategoriaFirebase(lCat.get_tituloCategoria(), lCat.get_idCategoria(), contCat))
            contPG = 0
            for pg in lCat.get_objectPerguntas():
                db.child(tabelaBanco).child(formNomeModelo).child("categorias").child(contCat).update(objectModeloFicha.updateFichaPerguntasFirebase(pg.get_tituloPergunta(), pg.get_tituloAlternativa(), contPG))
                contAlt = 0
                if pg.get_tituloAlternativa() == "dissertativa":
                    db.child(tabelaBanco).child(formNomeModelo).child("categorias").child(contCat).child("perguntas").child(contPG).update(objectModeloFicha.updateFichaDissertativaFirebase())
                else:
                    for alt in pg.get_tituloAlternativa():
                        db.child(tabelaBanco).child(formNomeModelo).child("categorias").child(contCat).child("perguntas").child(contPG).update(objectModeloFicha.updateFichaAlternativasFirebase(alt, contAlt))
                        contAlt = contAlt + 1
                contPG = contPG + 1
            contCat = contCat + 1

        return redirect(redirectModeloFicha)


    return render(request, "modeloFichas/manipularModeloFicha.html", data)


def excluirModeloFicha(request, modFichaExcluir):
    db.child(tabelaBanco).child(modFichaExcluir).remove()

    return redirect('/modeloFichas/')