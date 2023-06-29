from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('recovery', views.recovery, name="recovery"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.user_logout, name="logout"),
]