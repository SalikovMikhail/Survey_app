from django.urls import path
from .views import SurveyView, DetailSurveyView, StartSurveyAnonymView, AnswerFromUser, StartSurveyView, AnswerUserView


urlpatterns = [
    path('survey/', SurveyView.as_view()),
    path('survey/<int:pk>/', DetailSurveyView.as_view()),
    path('survey/startanonym/<int:pk>/', StartSurveyAnonymView.as_view()),
    path('survey/start/<int:pk>/', StartSurveyView.as_view()),
    path('question/answer/<int:pk>/', AnswerFromUser.as_view()),
    path('user/survey-answer/', AnswerUserView.as_view())
]
