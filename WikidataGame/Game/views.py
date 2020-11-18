from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import GenreForm, QuizForm
from .models import Question, Answer

from numpy.random import choice
import math
import random
import urllib.request
from bs4 import BeautifulSoup
import PyPDF2
from PIL import Image
import pytesseract


age_threshold = 200
confidence_threshold = 200


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


def genres(request):
    '''
    Provide a list of genres to display to the user
    '''

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


def get_genres(request):
    '''
    Helper function to obtain a list of genres
    '''

    gen_query_set = set(
        list(Question.objects.values_list('genre_name', flat=True)))
    genre_list = []

    for genre in gen_query_set:
        if genre:
            genre_list.append(genre)

    return genre_list


def quiz(request, genre):
    '''
    Obtain a list of questions by genre and display one question to the user by taking into account the age of the questions
    '''

    context = {}

    current_user = request.user
    context['user'] = User.objects.get(username=current_user)

    curr_question = pick_question(genre)
    context['question_object'] = curr_question.question_object
    context['question_property'] = curr_question.question_property

    context['genre'] = genre

    context['answers'] = list(Answer.objects.values_list(
        'answer', flat=True).filter(question_id=curr_question))

    form = QuizForm(request.POST, request.FILES)
    context['form'] = form

    if request.method == 'POST' and form.is_valid():
        answer = form.cleaned_data['answer']
        reference_url = form.cleaned_data['reference_url']
        reference_file = None
        try:
            reference_file = request.FILES['reference_file']
        except:
            pass
        check(curr_question, current_user, answer,
              reference_url, reference_file)
        return redirect('/quiz&' + genre)

    return render(request, 'quiz.html', context)


def pick_question(genre):
    '''
    Helper function to pick a question
    '''

    genre_questions = Question.objects.filter(
        genre_name=genre, is_updated=False)

    weights = []
    for question in genre_questions:
        if question.age == 0:
            weights.append(100000)
        else:
            weights.append(1/question.age)

    curr_question_list = random.choices(genre_questions, weights, k=1)
    curr_question = curr_question_list[0]

    return curr_question


def check(question, current_user, answer, reference_url, reference_file):
    '''
    Validate the answer provided by a user by cross checking with the reference provided and update the confidence score and trust score accordingly
    '''

    if answer == '':
        return

    answers = list(Answer.objects.values_list(
        'answer', flat=True).filter(question_id=question))

    if answer not in answers:
        if reference_url != '' or reference_file is not None:
            if reference_checker(reference_url, reference_file, question, answer):
                # reference is provided and answer matches with the reference so high confidence score is assigned and trust score is increased
                answer_obj = Answer(question_id=question,
                                    answer=answer, confidence_score=0.2)
                answer_obj.save()
                # current_user.trust_score += 0.5
            else:
                # reference is provided but answer does not match with the reference so low confidence score is assigned and trust score is decreased
                answer_obj = Answer(question_id=question,
                                    answer=answer, confidence_score=0.01)
                answer_obj.save()
                # current_user.trust_score -= 0.08

        else:
            answer_obj = Answer(question_id=question,
                                answer=answer, confidence_score=1/10)
            answer_obj.save()
            # current_user.trust_score += 0.05

    else:
        answer_obj = Answer.objects.get(answer=answer, question_id=question)
        if reference_url != '' or reference_file is not None:
            if reference_checker(reference_url, reference_file, question, answer):
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


def reference_checker(reference_url, reference_file, question, answer):
    '''
    Check if the answer exists in the reference 
    '''

    if reference_url != '':
        # reference url is provided
        try:
            f = urllib.request.urlopen(reference_url)
            content = f.read().decode('utf-8')
            soup = BeautifulSoup(content, features="html.parser")

            for script in soup(["script", "style"]):
                script.decompose()

            strips = list(soup.stripped_strings)

            if answer not in strips:
                return False
            else:
                return True
        except:
            return False

    else:
        # reference file is provided
        content = ''
        try:
            pdf_reader = PyPDF2.PdfFileReader(reference_file)
            num_pages = pdf_reader.numPages
            content = ''
            for page in range(0, num_pages):
                content += pdf_reader.getPage(page).extractText()
        except:
            img = Image.open(reference_file)
            content = pytesseract.image_to_string(img)

        tokens = content.split(" ")
        if answer not in tokens:
            return False
        else:
            return True


def aging(question, unique_answers, confidence_score):
    '''
    Update the age of a question based on number of views and uniue answers
    '''

    if confidence_score > confidence_threshold:
        question.is_updated = True

    new_views = question.number_of_views + 1
    new_age = question.age

    if unique_answers == 0:
        unique_answers = 1

    if new_views < 10:
        # less chances of having a definite answer, so less weightage to number of unique answers and their correctness
        new_age = 3 * new_views + \
            (10 * (1/unique_answers)) + (100 * math.pow(confidence_score-0.4, 2))
    else:
        new_age = 3 * new_views + \
            (50 * (1/unique_answers)) + (500 * math.pow(confidence_score-0.4, 2))

    if new_age > age_threshold:
        # update the question's answer in wikitable
        question.is_updated = True

    question.age = new_age
    question.number_of_views = new_views
    question.save()
    return
