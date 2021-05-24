from django.shortcuts import render, redirect
from LabGRis.decorators import validate_session, getSessionUser
from LabGRis.funcoesCompartilhadas import criarListaDoBanco, criarListaDoBancoKEY
from LabGRis.pyrebase_settings import db
from perguntas.classes.Perguntas import Pergunta
from categorias.classes.Categorias import Categoria
from responderFicha.classes.FichaPreenchida import FichaPreenchida


# Bancos
bancoModeloFicha = "Templates de Fichas"
tabelaBancoFicha = "fichaAppTeste"

# Redirecionamento de páginas
pgCampo = '/fichas/'

@validate_session
def responderFicha(request):
    data = {}
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    # Bancos
    bancoFicha = "fichaAppTeste"

    #########  Busca Modelos de Ficha já cadastradas
    fichaSalvas = db.child(bancoFicha).get()
    listaFicha = criarListaDoBanco(fichaSalvas)
    data['listaFicha'] = listaFicha

    print(listaFicha)

    return render(request, 'responderFicha/responderFicha.html', data)


@validate_session
def modelosFicha(request):
    data = {}
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    # Bancos
    bancoModeloFicha = "Templates de Fichas"

    #########  Busca Modelos de Ficha já cadastradas
    fichaSalvas = db.child(bancoModeloFicha).get()
    listaFicha = criarListaDoBanco(fichaSalvas)
    data['listaFicha'] = listaFicha

    return render(request, 'responderFicha/modelosFicha.html', data)


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
            try:
                for alter in perguntas["alternativas"]:
                    alternativaFicha = alter["tituloAlternativa"]
                    listaAlternativas.append(alternativaFicha)
            except:
                listaAlternativas.append("dissertativa")
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

    ################################################################ Recuperando informações do form ###################
    if request.method == "POST":
        listaPerguntasForm = []
        for perg in listaApenasPerguntas:
            pergunta = perg
            perguntaForm = request.POST.get(pergunta, 'Pergunta não carregada')
            resposta = ('resposta' + perg)
            respostaForm = request.POST.get(resposta, 'Resposta não carregada')
            tituloFicha = 'tituloFicha'
            tituloFichaForm = request.POST.get(tituloFicha, 'Titulo Ficha não carregada')
            tituloCategoriaF = 'tituloCategoria'
            tituloCategoriaForm = request.POST.get(tituloCategoriaF, 'Categoria não carregada')

            objectPerguntaPreenchida = Pergunta(perguntaForm, respostaForm)
            listaPerguntasForm.append(objectPerguntaPreenchida)

        ##################################################################### Salvando no banco
        contCat = 0
        objectFichaPreenchida = FichaPreenchida(tituloFichaForm, request.session.get('userId'), listaCategoriaSalvaFicha, fichaSelec)
        # Cria a ficha no banco
        db.child(tabelaBancoFicha).child(objectFichaPreenchida.get_tituloFicha()).set(objectFichaPreenchida.enviarFichaFirebase())
        # Percorre cada categoria
        for categoriaList in listaCategoriaSalvaFicha:
            idTeste = 0
            objectCategoriaPreenchida = Categoria(categoriaList.get_tituloCategoria(), idTeste, categoriaList.get_objectPerguntas())
            # Salva as categorias
            db.child(tabelaBancoFicha).child(objectFichaPreenchida.get_tituloFicha()).update(objectFichaPreenchida.updateFichaCategoriaFirebase(categoriaList.get_tituloCategoria(), idTeste, contCat))
            contP = 0
            for perg in objectCategoriaPreenchida.get_objectPerguntas():  # Salva as perguntas
                db.child(tabelaBancoFicha).child(objectFichaPreenchida.get_tituloFicha()).child('categorias').child(contCat).update(objectFichaPreenchida.updateFichaPerguntasFirebase(perg.get_tituloPergunta(), perg.get_tituloAlternativa(), contP))
                contAlt = 0
                for alter in perg.get_tituloAlternativa():  # Salva as alternativas
                    if alter == "dissertativa":
                        for pergForm in listaPerguntasForm:
                            if perg.get_tituloPergunta() == pergForm.get_tituloPergunta():
                                respostaDissertativa = pergForm.get_tituloAlternativa()
                        db.child(tabelaBancoFicha).child(objectFichaPreenchida.get_tituloFicha()).child('categorias').child(contCat).child('perguntas').child(contP).update(objectFichaPreenchida.updateFichaAlternativasDissertativaFirebase(respostaDissertativa, contAlt))

                    else:
                        marcadoComo = False
                        for pergForm in listaPerguntasForm:  # Salva a resposta (Para alterar resposta fazer algo parecido com este)
                            if perg.get_tituloPergunta() == pergForm.get_tituloPergunta():
                                if alter == pergForm.get_tituloAlternativa():
                                    marcadoComo = True
                        db.child(tabelaBancoFicha).child(objectFichaPreenchida.get_tituloFicha()).child('categorias').child(contCat).child('perguntas').child(contP).update(objectFichaPreenchida.updateFichaAlternativasFirebase(alter, contAlt, marcadoComo))

                    contAlt = contAlt + 1

                contP = contP + 1

            contCat = contCat + 1

        # html = "<html><body><center><h1>Pergunta:" + respostaForm + "</h1></center></body></html>"
        return redirect(pgCampo)

    return render(request, 'responderFicha/preencherFicha.html', data)