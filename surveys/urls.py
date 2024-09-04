from django.urls import path

from .views import AuthRegister,AuthLogin,SurveyAPIView,AuthUser

urlpatterns = [
    path('register', AuthRegister.as_view()),
    path('login', AuthLogin.as_view()),
    path('users', AuthUser.as_view()),
    path('users/<str:pk>', AuthUser.as_view()),
    path('surveys', SurveyAPIView.as_view()),
    path('surveys/<str:pk>', SurveyAPIView.as_view()),
]