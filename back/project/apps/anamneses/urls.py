from django.urls import path
from .views import *


urlpatterns = [
    path('question/', QuestionList.as_view(), name='question_list'),
    path('question/add', QuestionCreate.as_view(), name='question_create'),
    path('mold/', MoldList.as_view(), name='mold_list'),
    path('mold/add', MoldCreate.as_view(), name='mold_create'),
    path('anamnesis/', AnamnesisList.as_view(), name='anamnesis_list'),
    path('anamnesis/add', AnamnesisCreate.as_view(), name='anamnesis_create'),
    path('anamnesis/<uuid:student_id>/respond/<uuid:mold_id>', AnamnesisRespond.as_view(), name='anamnesis_respond')
]
