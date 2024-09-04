from django.urls import path

from .views import AuthRegister,AuthLogin,SurveyAPIView

urlpatterns = [
    path('register', AuthRegister.as_view()),
    path('login', AuthLogin.as_view()),
    path('surveys', SurveyAPIView.as_view()),
    path('surveys/<str:pk>', SurveyAPIView.as_view()),
]