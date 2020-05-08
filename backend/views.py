from django.http import HttpResponse
from django.shortcuts import render
from . import athenasrequest as athenas
import json


def login(request):
    if request.method == 'POST':
        database = athenas.show(request.POST['u'], request.POST['s'])
        return render(request, 'templates/index.html', {'database': database})
    return render(request, 'templates/login.html')


def api(request, u, p):
    dados = athenas.show(u, p)
    return HttpResponse(json.dumps(dados, indent=2), content_type='text')
