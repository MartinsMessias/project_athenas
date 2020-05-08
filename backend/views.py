from datetime import time

from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import athenasrequest as athenas
import json
import asyncio


# Create your views here.
def index(request, database):
    if database is not None:
        return render(request, 'templates/index.html', {'database': database, 'datalog':database[-1]})
    return redirect(login)


def login(request):
    if request.method == 'POST':
        database = athenas.show(request.POST['u'], request.POST['s'])
        asyncio.sleep(5)
        return index(request=request, database=database)
    return render(request, 'templates/login.html')


def api(request, u, p):
    dados = athenas.show(u, p)
    asyncio.sleep(1)
    return HttpResponse(dados)
