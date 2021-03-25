from django.shortcuts import render

# Create your views here.

def main(request):
    data = {}
    #data['SessionUser'] = getSessionUser(request)
    data['context'] = ""
    return render(request, 'main/main.html')