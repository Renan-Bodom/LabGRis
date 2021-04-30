from django.shortcuts import render, redirect
from LabGRis.decorators import validate_session, getSessionUser
from LabGRis.funcoesCompartilhadas import criarListaDoBanco, criarListaDoBancoKEY
from LabGRis.pyrebase_settings import db
import datetime

# Bancos
bancoCategoria = "categoria"

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

    # Bancos
    bancoCategoria = "categoria"

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    #########  Busca perguntas para listar no dualList
    perguntasSalvas = db.child("perguntas").get()
    listaPerguntas = criarListaDoBanco(perguntasSalvas)

    apenasPerguntas = []
    for perguntas in listaPerguntas:
        apenasPerguntas.append(perguntas['enunciado'])

    data['listaPerguntas'] = apenasPerguntas


    ###### Capta informações do form
    tituloCategoria = 'nomeCategoria'
    formTituloCategoria = request.POST.get(tituloCategoria, 'Categoria não carregada')
    idCategoriaMae = 'idCategoriaMae'
    formIdCategoriaMae = request.POST.get(idCategoriaMae, 'ID Categoria Mãe não carregada')
    SelPerguntas = 'SelPerguntas'
    formSelPerguntas = request.POST.getlist(SelPerguntas, 'Perguntas não carregada')


    print('Titulo cat:', formTituloCategoria, ' ID:', formIdCategoriaMae, ' Perguntas:', formSelPerguntas)


    ###### Identifica o botão salvar e cadastra no banco
    if request.method == "POST" and "cadastrarCategoria" in request.POST:
        '''
        listaObjectPerguntas = []
        for per in formSelPerguntas:
            perguntasDoBanco = db.child("perguntas").child(per).get()
            perguntaEAlternativas = criarListaDoBanco(perguntasDoBanco)
            objectPergunta = Pergunta(perguntaEAlternativas[1], perguntaEAlternativas[0])
            listaObjectPerguntas.append(objectPergunta)

        objectCategoria = Categoria(formTituloCategoria, formIdCategoriaMae, listaObjectPerguntas)
        listaPerguntas = objectCategoria.get_objectPerguntas()

        db.child(bancoCategoria).child(formTituloCategoria).set(objectCategoria.enviarCategoriaFirebase())
        for per in listaPerguntas:
            db.child(bancoCategoria).child(formTituloCategoria).update(
                objectCategoria.updatePerguntasCategoriaFirebase(per.get_tituloPergunta(), per.get_tituloAlternativa()))'''

        return redirect('/categorias/')

    return render(request,'categorias/manipularCategoria.html', data)


def alterarCategoria(request, categoria):
    print('Alterar categoria:', categoria)

    return redirect(redirectCat)

def excluirCategoria(request, categoria):
    print('Excluir categoria:', categoria)
    #db.child(bancoCategoria).child(categoria).remove()

    return redirect(redirectCat)