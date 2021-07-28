from django.shortcuts import render, redirect
import pandas as pd
import datetime
from django.http import HttpResponse
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

    #########  Busca Modelos de Ficha já cadastradas
    fichaSalvas = db.child(tabelaBancoFicha).get()
    listaFicha = criarListaDoBanco(fichaSalvas)
    data['listaFicha'] = listaFicha

    if request.method == "POST":
        codFicha = request.POST.getlist('codFicha', 'Pergunta não carregada')

        # Lista para colocar dados das fichas
        modeloFicha = []
        tituloFicha = []
        perguntasDasFichas = set()
        # Carregando dados das fichas selecionadas
        for ficha in codFicha:
            dadosDaFicha = db.child(tabelaBancoFicha).child(ficha).get().val()

            modeloFicha.append(dadosDaFicha['modeloFicha'])
            tituloFicha.append(dadosDaFicha['tituloFicha'])

            for cat in dadosDaFicha['categorias']:
                for per in cat['perguntas']:
                    perguntasDasFichas.add(per['tituloPergunta'])

        print('Perguntas', perguntasDasFichas)
        for perF in perguntasDasFichas:
            for ficha in codFicha:
                dadosCat = db.child(tabelaBancoFicha).child(ficha).child('categorias').get().val()
                for cat in dadosCat:
                    for perg in cat['perguntas']:
                        if perg['tituloPergunta'] == perF:
                            try:
                                print("Diss:", perg['resposta'])
                            except:
                                for alt in perg['alternativas']:
                                    if alt['resposta'] == True:
                                        print("Alt:", alt['tituloAlternativa'])


        # Montando o dicionario para converter em DataFrame
        dadosFichas = {
            'Modelo ficha': modeloFicha,
            'Ficha':        tituloFicha
            }


        # Transformando os dados em um DataFrame
        dadosFicha_df = pd.DataFrame(data=dadosFichas)
        print("DataFrame da(s) fichas:\n", dadosFicha_df)

        # Disponibilizando CSV para download
        responseCSV = HttpResponse(content_type='text/csv')
        responseCSV['Content-Disposition'] = 'attachment; filename=CSV_LabGRis ' + datetime.datetime.now().strftime('%d/%m/%Y') + '.csv'
        dadosFicha_df.to_csv(path_or_buf=responseCSV, index=False)

        return responseCSV
        #return redirect(pgCampo)

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


def excluirFicha(request, fichaSelec):
    db.child(tabelaBancoFicha).child(fichaSelec).remove()

    return redirect('url_responderFicha')

def alterarFicha(request, fichaSelec):
    data = {}
    data['SessionUser'] = getSessionUser(request)

    dadosFicha = db.child(tabelaBancoFicha).child(fichaSelec).get().val()
    data['fichaSelec'] = dadosFicha

    contListaCategBanco = len(dadosFicha['categorias'])

    listaApenasPerguntas = []
    for categorias in dadosFicha['categorias']:
        for perguntas in categorias['perguntas']:
            listaApenasPerguntas.append(perguntas['tituloPergunta'])

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


        ########## Listando categorias
        listaCategoriaSalvaFicha = []
        for ContFor in range(contListaCategBanco):
            categoriaDoBanco = db.child(tabelaBancoFicha).child(fichaSelec).child("categorias").child(
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

        ##################################################################### Salvando no banco
        contCat = 0
        objectFichaPreenchida = FichaPreenchida(tituloFichaForm, request.session.get('userId'),
                                                listaCategoriaSalvaFicha, fichaSelec)
        # Cria a ficha no banco
        db.child(tabelaBancoFicha).child(objectFichaPreenchida.get_tituloFicha()).set(
            objectFichaPreenchida.enviarFichaFirebase())

        # Percorre cada categoria
        for categoriaList in listaCategoriaSalvaFicha:
            idTeste = 0
            objectCategoriaPreenchida = Categoria(categoriaList.get_tituloCategoria(), idTeste,
                                                  categoriaList.get_objectPerguntas())
            # Salva as categorias
            db.child(tabelaBancoFicha).child(objectFichaPreenchida.get_tituloFicha()).update(
                objectFichaPreenchida.updateFichaCategoriaFirebase(categoriaList.get_tituloCategoria(), idTeste,
                                                                   contCat))
            contP = 0
            for perg in objectCategoriaPreenchida.get_objectPerguntas():  # Salva as perguntas
                db.child(tabelaBancoFicha).child(objectFichaPreenchida.get_tituloFicha()).child('categorias').child(
                    contCat).update(objectFichaPreenchida.updateFichaPerguntasFirebase(perg.get_tituloPergunta(),
                                                                                       perg.get_tituloAlternativa(),
                                                                                       contP))
                contAlt = 0
                for alter in perg.get_tituloAlternativa():  # Salva as alternativas
                    if alter == "dissertativa":
                        for pergForm in listaPerguntasForm:
                            if perg.get_tituloPergunta() == pergForm.get_tituloPergunta():
                                respostaDissertativa = pergForm.get_tituloAlternativa()
                        db.child(tabelaBancoFicha).child(objectFichaPreenchida.get_tituloFicha()).child(
                            'categorias').child(contCat).child('perguntas').child(contP).update(
                            objectFichaPreenchida.updateFichaAlternativasDissertativaFirebase(respostaDissertativa,
                                                                                              contAlt))

                    else:
                        marcadoComo = False
                        for pergForm in listaPerguntasForm:  # Salva a resposta (Para alterar resposta fazer algo parecido com este)
                            if perg.get_tituloPergunta() == pergForm.get_tituloPergunta():
                                if alter == pergForm.get_tituloAlternativa():
                                    marcadoComo = True
                        db.child(tabelaBancoFicha).child(objectFichaPreenchida.get_tituloFicha()).child(
                            'categorias').child(contCat).child('perguntas').child(contP).update(
                            objectFichaPreenchida.updateFichaAlternativasFirebase(alter, contAlt, marcadoComo))

                    contAlt = contAlt + 1

                contP = contP + 1

            contCat = contCat + 1

        # html = "<html><body><center><h1>Pergunta:" + respostaForm + "</h1></center></body></html>"

        return redirect('url_responderFicha')


    return render(request, 'responderFicha/alterarFicha.html', data)