from django.shortcuts import render
from LabGRis.decorators import validate_session, getSessionUser

@validate_session
def perguntas(request):
    data = {}
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""
    return render(request,'perguntas/perguntas.html', data)