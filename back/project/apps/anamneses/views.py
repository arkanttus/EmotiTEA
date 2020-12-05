from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .models import *
from .forms import *


User = get_user_model


class QuestionCreate(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'anamneses/question_create.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.get_form_class())

        question_form = QuestionFormSet()

        return self.render_to_response(
            self.get_context_data(
                question_form=question_form
            )
        )

        #if form.is_valid():
            
