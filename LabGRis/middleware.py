from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.http import HttpResponse


# FILTRA IP MIDDLEWARE
# ----------------------------------------

class ValidarLogin:

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path_info.lstrip('/')
        print(path)
        if not request.session.get('userId'):
            return redirect('/access/login/')

        return None


class getSessionUser:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        self.info_user = {
            'user': request.session.get('user'),
            'username': request.session.get('username'),
            'name': request.session.get('name')
        }
        response.context_data["info_user"] = self.info_user
        return response
