from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import random
from .forms import GenreForm, QuizForm
from .models import Question, Answer
import urllib.request
from bs4 import BeautifulSoup
import math

age_threshold = 200

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
    context = {}
    current_user = request.user
    context['user'] = User.objects.get(username=current_user)
    return render(request, 'home.html', context)


def get_genres(request):
    gen_query_set = set(
        list(Question.objects.values_list('genre_name', flat=True)))
    genre_list = []

    for genre in gen_query_set:
        if genre:
            genre_list.append(genre)

    return genre_list


def genres(request):
    context = {}

    current_user = request.user
    context['user'] = User.objects.get(username=current_user)

    context['genres'] = get_genres(request)

    form = GenreForm(request.POST)
    context['form'] = form

    if request.method == 'POST' and form.is_valid():
        genre = form.cleaned_data['genre']
        return redirect('/quiz&' + genre)

    return render(request, 'genres.html', context)


def aging(question, unique_answers, confidence_score):

    ## for a given question we need to take into account the number of users we have shown the question till now, the number of unique answers and the confidence among those answers. 

    ## input -> Question
    ## output -> Question's age

    new_views = question.number_of_views + 1
    new_age = question.age

    ## the confidence score among all the various answers will be following a quadratic type of curve, where it will be responsible for aging if the score is too high or too low and less weight if it lies somewhere in middle. 

    if new_views < 10:
        
        ## less chances of having a definite answer, so less weightage to number of unique answers and thier correctness
        new_age = 3 * new_views + (10 * (1/unique_answers)) + (100 * math.pow(confidence_score-0.4,2))
    else:
        new_age = 3 * new_views + (50 * (1/unique_answers)) + (500 * math.pow(confidence_score-0.4,2))
        

    if new_age > age_threshold:

        ### TO BE ADDED ## update the question's answer into the wikitable using the bot from here.
        question.is_updated = True

    question.age = new_age
    question.number_of_views = new_views
    question.save()
    return

def pick_questions(genre):
    pass



def quiz(request, genre):
    context = {}

    current_user = request.user
    context['user'] = User.objects.get(username=current_user)

    genre_questions = Question.objects.filter(genre_name=genre)
    total_questions = len(genre_questions)


    ## here, the questions will be ranked according to their age and among the top aged question, we will randomly pick from top 3.
    num = random.randint(0, total_questions - 1)

    curr_question = genre_questions[num]
    context['question_hin'] = curr_question.question_hin
    context['genre'] = genre

    form = QuizForm(request.POST)
    context['form'] = form

    if request.method == 'POST' and form.is_valid():
        answer = form.cleaned_data['answer']
        reference = form.cleaned_data['reference']
        check(curr_question, current_user, answer, reference)
        return redirect('/quiz&' + genre)

    return render(request, 'quiz.html', context)


def check(question, current_user, answer = None, reference = None):

    if answer is None:
        return 

    question_text = question.question_hin
    question_id = question.question_id
    # prev_trust = current_user.trust_score
    answers = list(Answer.objects.values_list('answer', flat=True).filter(question_id=question))
    print(answers)

    # if answer does not exist
    if answer not in answers:
        if reference is not None:
            if reference_checker(reference, question, answer):
                answer_obj = Answer(question_id=question, answer=answer, confidence_score=0.2)
                answer_obj.save()
                # current_user.trust_score += 0.5
            else:
                answer_obj = Answer(question_id=question, answer=answer, confidence_score=0.01)
                answer_obj.save()
                # current_user.trust_score -= 0.08
        else:
            answer_obj = Answer(question_id=question, answer=answer, confidence_score=1/10)
            answer_obj.save()
            # current_user.trust_score += 0.05
    else:
        answer_obj = Answer.objects.get(answer=answer,question_id=question)
        if reference is not None:
            # check which answer is the most used and score accordingly, also trust score will play a role here
            # print(answer_list)
            if reference_checker(reference, question, answer):
                answer_obj.confidence_score += 0.2
                # current_user.trust_score += 0.3
            else:
                answer_obj.confidence_score += 0.08
                # current_user.trust_score -= 0.1
        else:
            answer_obj.confidence_score += 0.1
            # current_user.trust_score += 0.08
        answer_obj.save()

    best_answer_confidence = 0
    aging(question, len(answers), best_answer_confidence)
                    
            

def reference_checker(reference, question, answer):
    f = urllib.request.urlopen(reference)
    content = f.read().decode('utf-8')
    soup = BeautifulSoup(content, features="html.parser")

    for script in soup(["script","style"]):
        script.decompose()

    strips = list(soup.stripped_strings)
    question_text = question.question_hin
    question_tokens = question_text.split(' ')
    key_terms = [question_tokens[1], question_tokens[2], answer]

    if answer not in strips:
        return False
    else:
        return True
