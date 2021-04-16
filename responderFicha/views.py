from django.shortcuts import render
from LabGRis.decorators import validate_session, getSessionUser
from LabGRis.funcoesCompartilhadas import criarListaDoBanco, criarListaDoBancoKEY
from LabGRis.pyrebase_settings import db
from perguntas.classes.Perguntas import Pergunta
from categorias.classes.Categorias import Categoria


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


def preenchendoFicha(request, fichaSelec):
    data = {}
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""
    data['ficha'] = fichaSelec

    # Bancos
    bancoModeloFicha = "Templates de Fichas"

    ######### Busca categorias salva por ficha e conta o número de categoria
    BuscaCategBanco = db.child(bancoModeloFicha).child(fichaSelec).child("categorias").get()
    listaCategBanco = criarListaDoBancoKEY(BuscaCategBanco)
    contListaCategBanco = len(
        listaCategBanco)  # Categorias são númeradas no banco, para encontrar todas precisa saber quantas tem

    ########## Listando categorias
    listaCategoriaSalvaFicha = []
    for ContFor in range(contListaCategBanco):
        categoriaDoBanco = db.child(bancoModeloFicha).child(fichaSelec).child("categorias").child(
            ContFor).get()  # Encontra cada categoria da ficha selecionada
        categoriaSalvaFicha = criarListaDoBanco(categoriaDoBanco)  # Carrega os dados da categoria
        tituloCategoria = categoriaSalvaFicha[1]  # Título categoria
        perguntasFicha = categoriaSalvaFicha[0]  # Perguntas da categoria

        perguntaDaLista = []
        for per in perguntasFicha:
            perguntaDaLista.append(per)
        listaDePerguntas = []
        for perguntas in perguntaDaLista:
            listaAlternativas = []
            for alter in perguntas["alternativas"]:
                alternativaFicha = alter["tituloAlternativa"]
                listaAlternativas.append(alternativaFicha)
            objectPerguntas = Pergunta(perguntas["tituloPergunta"], listaAlternativas)
            listaDePerguntas.append(objectPerguntas)
        objectCategoria = Categoria(tituloCategoria, 1, listaDePerguntas)
        listaCategoriaSalvaFicha.append(objectCategoria)

    ############################ Organizando perguntas para enviar ao template ######################################
    listaApenasPerguntas = []  # Lista contendo todas as perguntas, sem nenhum criterio
    listaPergutas = []  # Lista com [[[Cat1],[perguntas e respostas]],[[Cat2], [perguntas e respostas]]]
    for cat in listaCategoriaSalvaFicha:
        juntaInfPerguntas = []
        juntaInfPerguntas.append([cat.get_tituloCategoria()])
        juntPerguntas = []
        for perg in cat.get_objectPerguntas():
            juntPerguntas.append({"pergunta": perg.get_tituloPergunta(), "alternativas": perg.get_tituloAlternativa})
            listaApenasPerguntas.append(perg.get_tituloPergunta())
        juntaInfPerguntas.append(juntPerguntas)
        listaPergutas.append(juntaInfPerguntas)

    data['categoriaSelec'] = listaPergutas

    return render(request, 'responderFicha/preencherFicha.html', data)