from datetime import time

from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import athenasrequest as athenas
import json
import asyncio


# Create your views here.
async def index(request, database):
    global datalog
    if database is not None:
        return render(request, 'templates/index.html', {'database': database, 'datalog':data_log})
    return redirect(login)


async def login(request):
    global database
    global data_log
    if request.method == 'POST':
        database, data_log = None, None
        database, data_log = await athenas.show(request.POST['u'], request.POST['s'])
        return index(request=request, database=database)
    return render(request, 'templates/login.html')


def api(request, u, p):
    dados, data_log = athenas.show(u, p)
    asyncio.sleep(1)
    return HttpResponse(dados)
