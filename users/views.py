from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import sys, datetime
from LabGRis.pyrebase_settings import db, auth
from LabGRis.decorators import validate_session, getSessionUser
from LabGRis.decorators import clear_session

# Bancos
bancoUsers = "users"

#@validate_session
def users(request):
    return render(request,'users/users.html')

def login(request):
    return render(request, 'users/login.html')


def valida_senha(request):
    email = request.POST.get('txtUserEmail', '')
    senha = request.POST.get('txtUserPassword', '')
    try:

        sign_user = auth.sign_in_with_email_and_password(email, senha)
        sign_user = auth.refresh(sign_user['refreshToken'])

        userLab = db.child("users").child(sign_user['userId']).get()

        request.session['idToken'] = sign_user['idToken']
        request.session['userEmail'] = email
        request.session['userId'] = sign_user['userId']
        request.session['nomeUsuario'] = userLab.val()['nome']
        request.session['perfilUsuario'] = userLab.val()['perfil']

        # Verificando se tem solicitação para excluir usuário
        excluirUser = db.child(bancoUsers).child(sign_user['userId']).child("excluirUser").get().val()
        if excluirUser == True:
            auth.delete_user_account(sign_user['idToken'])
            # db.child(bancoUsers).child(sign_user['userId']).remove()
            return render(request, "users/mensagens.html", {'user': userLab.val()['nome']})


    except:
        print("Entrou AQUI")
        clear_session(request)
        print(sys.exc_info()[1])
        messages.error(request, "Usuário ou senha inválidos!")
        return redirect('/usuario/entrar/')

    return redirect('/')


def sair (request):
    # for key in request.session.keys():
    # del request.session[key]
    clear_session(request)

    return render(request, "users/login.html")

@validate_session
def listaUsers (request):
    data = {}   # Dicionário DJango


    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    #  Carrega usuário já cadastrado
    usuariosSalvos = db.child(bancoUsers).get()
    listaUsuarios = []
    for dadosUser in usuariosSalvos.each():
        dadosUser2 = dadosUser.val()
        dadosUser2['key'] = dadosUser.key()
        # Ocultando usuário marcados com exclusão
        if dadosUser.val()['excluirUser'] == True:
            dadosUser2 = None
        else:
            listaUsuarios.append(dadosUser2)

    data['listaUsuarios'] = listaUsuarios

    return render(request, "users/listarUsers.html", data)

@validate_session
def novoUsuario (request):
    data = {}  # Dicionário DJango
    data['datenow'] = [datetime.datetime.now().strftime('%d/%m/%Y'), datetime.datetime.now().strftime('%H:%M:%S')]

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""


    # Salvar usuário
    if request.method == "POST":
        data = request.POST.get('data', '')
        nome = request.POST.get('nome', '')
        perfil = request.POST.get('perfil', '')
        cpf = request.POST.get('cpf', '')
        email = request.POST.get('email', '')
        locaisFrequentados = request.POST.get('locaisFrequentados', '')

        # Verificando se e-mail já foi cadastrado
        try:
            sign_user = auth.create_user_with_email_and_password(email, 'labgris123')
        except:
            return HttpResponse("<html><body><center>E-mail cadastrado!<br>" + email + "<br><br>"
                                "Mudar excluirUser para false no banco<br><br>"
                                "<a href='/usuario/listar/'>Voltar</a></center></body></html>")
        sign_user = auth.refresh(sign_user['refreshToken'])
        userId = sign_user['userId']


        formCadastro = {'data': data,
                        'nome': nome,
                        'excluirUser': False,
                        'perfil': perfil,
                        'cpf': cpf,
                        'email': email,
                        'locaisFrequentados': locaisFrequentados}
        db.child(bancoUsers).child(userId).set(formCadastro)

        return redirect('/usuario/listar/')

    return render(request, "users/manipularUsuario.html", data)

def alterarUsuario(request, userAlterar):
    data = {}  # Dicionário DJango
    data['datenow'] = [datetime.datetime.now().strftime('%d/%m/%Y'), datetime.datetime.now().strftime('%H:%M:%S')]

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    # Dados do usuario
    data['dadosUsuario'] = db.child(bancoUsers).child(userAlterar).get().val()

    # Salvar usuário
    if request.method == "POST":
        data = request.POST.get('data', '')
        nome = request.POST.get('nome', '')
        perfil = request.POST.get('perfil', '')
        cpf = request.POST.get('cpf', '')
        locaisFrequentados = request.POST.get('locaisFrequentados', '')

        formCadastro = {'data': data,
                        'nome': nome,
                        'perfil': perfil,
                        'cpf': cpf,
                        'locaisFrequentados': locaisFrequentados}
        db.child(bancoUsers).child(userAlterar).update(formCadastro)
        return redirect('/usuario/listar/')

    return render(request, "users/alterarUsuario.html", data)

def removerUsuario(request, userRemover):
    data = {}

    # Remover informações do banco
    excluirUser = {'excluirUser': True}
    db.child(bancoUsers).child(userRemover).update(excluirUser)

    #db.child('usersParaRemover').update({"userId " + userRemover: userRemover})

    return redirect('/usuario/listar/')

def esqueciSenha(request):
    data = {}

    if request.method == "POST":
        email = request.POST.get('txtUserEmail', '')
        auth.send_password_reset_email(email)

        return HttpResponse("<html><body><center>Verifique seu e-mail:<br>" + email +
                            "<br><br><a href='/usuario/entrar/'>Voltar</a></center></body></html>")

    return render(request, "users/esqueceuSenha.html", data)