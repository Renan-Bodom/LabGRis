from pyrebase_settings import db, auth
from django.shortcuts import redirect


def validate_session(function):
    def validate_user(request):
        if not request.session.get('userId'):
            return redirect('/usuario/entrar/')

        return function(request)

    return validate_user


def retornaAcessos(request):
    acessos = db.child("perfil").child(request.session.get('perfilUsuario')).child('modulos').get()
    listLocal = []
    data = {}
    try:
        for alt in acessos.each():
            item = {
                "modulo": alt.key(),
                "data": alt.val()
            }
            listLocal.append(item)

        data['list'] = listLocal
    except:
        data = {}

    return data


def getSessionUser(request):
    data = {'userIdAuth': request.session.get('userIdAuth'),
            'userId': request.session.get('userId'),
            'idToken': request.session.get('idToken'),
            'userEmail': request.session.get('userEmail'),
            'nomeUsuario': request.session.get('nomeUsuario'),
            'perfilUsuario': request.session.get('perfilUsuario'),
            'perfilUsuarioModulos': retornaAcessos(request)}
    print(data)
    return data


def clear_session(request):
    if request.session.get('userId'):
        del request.session['userId']

    if request.session.get('idToken'):
        del request.session['idToken']

    if request.session.get('userEmail'):
        del request.session['userEmail']

    if request.session.get('userId'):
        del request.session['userId']

    if request.session.get('nomeUsuario'):
        del request.session['nomeUsuario']

    if request.session.get('perfilUsuario'):
        del request.session['perfilUsuario']

    return request
