from django.urls import path

from . import views

urlpatterns = [
    path("", views.signUp, name="signUp"),
    path("login/", views.logIn, name="logIn")
]