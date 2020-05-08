from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import athenasrequest as athenas

database = None


# Create your views here.
def index(request):
    global database
    if database is not None:
        return render(request, 'templates/index.html', {'database': database})
    database = None
    return redirect(login)


def login(request):
    global database
    if request.method == 'POST':
        database = None
        database = athenas.show(request.POST['u'], request.POST['s'])
        return index(request=request)
    return render(request, 'templates/login.html')
