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
        question_form = QuestionFormSet(queryset=Question.objects.none())

        return self.render_to_response(
            self.get_context_data(
                question_form=question_form
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        question_form = QuestionFormSet(request.POST)
        
        if question_form.is_valid():
            print(question_form.cleaned_data)
            print('VLAIDO')
            question_form.save()
            return redirect(self.template_name)
        else:
            return self.render_to_response(
                self.get_context_data(
                    question_form=question_form
                )
            )


class MoldCreate(CreateView):
    model = Mold
    form = MoldForm
    template_name = 'anamneses/mold_create.html'
