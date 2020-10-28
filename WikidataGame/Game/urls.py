from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Game/sign_up/', views.sign_up, name="sign-up"),
    path('home', views.home, name='home'),
    path('genres', views.genres, name='genres'),
    # path('quiz', views.quiz, name='quiz'),
]

urlpatterns += staticfiles_urlpatterns()
