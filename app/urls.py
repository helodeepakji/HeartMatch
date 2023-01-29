from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('findbest', views.findbest, name='findbest'),
    path('profile', views.profile, name='profile'),
    path('contact', views.contact, name='contact'),
    path('login', views.userlogin, name='login'),
    path('logout', views.userlogout, name='logout'),
    path('regisiter', views.regisiter, name='regisiter'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('addFriend', views.addFriend, name='addFriend'),
    path('acceptFriend', views.acceptFriend, name='acceptFriend'),
]