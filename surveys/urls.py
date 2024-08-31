from django.urls import path

from .views import AuthRegister,AuthLogin

urlpatterns = [
    path('/register', AuthRegister.as_view()),
    path('/login', AuthLogin.as_view()),
]