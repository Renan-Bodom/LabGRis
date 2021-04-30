from django.shortcuts import render, redirect
from django.contrib import messages
import sys, datetime
from LabGRis.pyrebase_settings import db, auth
from LabGRis.decorators import validate_session, getSessionUser
from LabGRis.decorators import clear_session

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

    # Bancos
    tabelaUsers = "users"

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    #  Carrega usuário já cadastrado
    usuariosSalvos = db.child(tabelaUsers).get()
    listaUsuarios = []
    for alt in usuariosSalvos.each():
        listaUsuarios.append(alt.val())

    data['listaUsuarios'] = listaUsuarios

    return render(request, "users/listarUsers.html", data)

@validate_session
def novoUsuario (request):
    data = {}  # Dicionário DJango
    data['datenow'] = [datetime.datetime.now().strftime('%d/%m/%Y'), datetime.datetime.now().strftime('%H:%M:%S')]

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    # Bancos
    bancoUsers = "users"

    # Salvar usuário
    if request.method == "POST":
        data = request.POST.get('data', '')
        nome = request.POST.get('nome', '')
        perfil = request.POST.get('perfil', '')
        cpf = request.POST.get('cpf', '')
        email = request.POST.get('email', '')
        locaisFrequentados = request.POST.get('locaisFrequentados', '')

        sign_user = auth.create_user_with_email_and_password(email, 'labgris123')
        sign_user = auth.refresh(sign_user['refreshToken'])
        userId = sign_user['userId']


        formCadastro = {'data': data,
                        'nome': nome,
                        'perfil': perfil,
                        'cpf': cpf,
                        'email': email,
                        'locaisFrequentados': locaisFrequentados}
        db.child(bancoUsers).child(userId).set(formCadastro)

        return redirect('/usuario/listar/')

    return render(request, "users/manipularUsuario.html", data)

def alterarUsuario(request):
    data = {}  # Dicionário DJango
    data['datenow'] = [datetime.datetime.now().strftime('%d/%m/%Y'), datetime.datetime.now().strftime('%H:%M:%S')]

    # Parte do decorators de login
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    # Bancos
    bancoUsers = "users"

    # Salvar usuário
    if request.method == "POST":
        data = request.POST.get('data', '')
        nome = request.POST.get('nome', '')
        perfil = request.POST.get('perfil', '')
        cpf = request.POST.get('cpf', '')
        email = request.POST.get('email', '')
        locaisFrequentados = request.POST.get('locaisFrequentados', '')

        formCadastro = {'data': data,
                        'nome': nome,
                        'perfil': perfil,
                        'cpf': cpf,
                        'locaisFrequentados': locaisFrequentados}
        db.child(bancoUsers).child(request.session.get('userId')).update(formCadastro)

    return render(request, "users/manipularUsuario.html", data)