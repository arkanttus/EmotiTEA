from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import *
from .forms import *
from apps.base.models import Institution

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
            questions_instances = question_form.save(commit=False)

            for obj in question_form.deleted_objects:
                obj.delete()

            for question in questions_instances:
                question.institution = Institution.objects.get(id='5b62de2b-d096-41e6-991b-6f9bbb25964f')

            Question.objects.bulk_create(questions_instances)

            return redirect(self.template_name)
        else:
            return self.render_to_response(
                self.get_context_data(
                    question_form=question_form
                )
            )


class MoldCreate(CreateView):
    model = Mold
    form_class = MoldForm
    template_name = 'anamneses/mold_create.html'

    def get(self, request):
        self.object = None
        self.questions = Question.objects.filter(Q(institution__id='5b62de2b-d096-41e6-991b-6f9bbb25964f') | Q(institution__id__isnull=True))

        form = self.get_form(self.get_form_class())

        return self.render_to_response(
            self.get_context_data(
                form=form
            )
        )
    
    def post(self, request):
        self.object = None
        institution = Institution.objects.get(id='5b62de2b-d096-41e6-991b-6f9bbb25964f')
        self.questions = Question.objects.filter(Q(institution=institution) | Q(institution__id__isnull=True))

        form = self.get_form(self.get_form_class())

        if form.is_valid():
            print(form.cleaned_data)
            form_instance = form.save(commit=False)
            form_instance.institution = institution
            
            print(form_instance.__dict__)

            form_instance.save()
            form.save_m2m()
        else:
            return self.render_to_response(
                self.get_context_data(
                    form=form
                )
            )

    def get_form_kwargs(self):
        kwargs = super(MoldCreate, self).get_form_kwargs()
        kwargs['question_queryset'] = self.questions
        return kwargs
