from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views



from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required



@login_required
def index(request):
    return render(request,'Game/index.html')


def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request,user)
            return render(request,'Game/index.html')
    context['form']=form
    return render(request,'registration/sign_up.html',context)