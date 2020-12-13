from django.urls import path
from .views import *


urlpatterns = [
    path('question/add', QuestionCreate.as_view(), name='question_create'),
    path('mold/add', MoldCreate.as_view(), name='mold_create'),
]
