from django.shortcuts import render
from LabGRis.decorators import validate_session, getSessionUser


@validate_session
def categorias(request):
    data = {}
    data['SessionUser'] = getSessionUser(request)
    data['context'] = ""

    return render(request, 'categorias/categorias.html', data)