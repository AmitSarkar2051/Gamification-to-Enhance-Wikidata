from django.contrib import admin 
from django.urls import path, include 
from . import views 
from django.contrib.auth import views as auth 
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [ 
    path('', views.index, name ='index'), 
    path('login/', views.Login, name ='login'), 
    path('logout/', auth.LogoutView.as_view(template_name ='user/index.html'), name ='logout'), 
    path('register/', views.register, name ='register'), 
] 
