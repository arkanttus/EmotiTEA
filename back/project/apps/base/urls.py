from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='dashboard'),
    path('student/', StudentList.as_view(), name='student_list'),
    path('student/add', StudentCreate.as_view(), name='student_create'),
]
