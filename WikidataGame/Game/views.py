from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import random
from .forms import GenreForm
from .models import Question, Answer


@login_required
def index(request):
    return render(request, 'Game/index.html')


def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'Game/index.html')
    context['form'] = form
    return render(request, 'registration/sign_up.html', context)


def home(request):
    current_user = request.user
    context = {}
    context['user'] = User.objects.get(username=current_user)
    return render(request, 'home.html', context)


def genres(request):
    context = {}
    context['genres'] = ['Maths', 'Computer', 'Chemistry']
    form = GenreForm(request.POST)
    context['form'] = form

    if request.method == 'POST' and form.is_valid():
        genre = form.cleaned_data['genre']
        print(genre)
        return redirect('/game/quiz/' + genre)

    return render(request, 'genres.html', context)


def quiz(request, genre):
    print(genre)
    context = {}
    genre_questions = Question.objects.filter(genre_name=genre)
    total_questions = len(genre_questions)
    print(total_questions, genre_questions)
    num = random.randint(0, total_questions - 1)
    print(num)
    context['question_hin'] = genre_questions[num]
    context['genre'] = genre
    return render(request, 'quiz.html', context)
