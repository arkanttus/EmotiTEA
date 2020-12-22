from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import *
from .forms import *
from apps.base.models import Institution


User = get_user_model


class AnamnesisList(ListView):
    model = Anamnesis
    template_name = 'anamneses/anamneses_list.html'

    def get_queryset(self):
        return Anamnesis.objects.filter(institution=self.request.user.institution)


class AnamnesisCreate(SuccessMessageMixin, CreateView):
    model = Anamnesis
    form_class = AnamnesisForm
    template_name = 'anamneses/anamneses_create.html'
    success_url = reverse_lazy('anamnesis_list')
    success_message = 'Anamnese criada com sucesso!'

    def get(self, request, *args, **kwargs):
        self.object = None
        institution = request.user.institution

        self.students = institution.students
        self.molds = Mold.objects.filter(institution=institution)

        if self.students.count() == 0:
            messages.error(request, "Nenhum estudante cadastrado!")
            return redirect('anamnesis_list')
        if self.molds.count() == 0:
            messages.error(request, "Nenhum Molde de Questões criado!")
            return redirect('anamnesis_list')

        form = self.get_form(self.get_form_class())

        return self.render_to_response(
            self.get_context_data(
                form=form
            )
        )
    
    def post(self, request):
        self.object = None
        institution = request.user.institution
        
        self.students = institution.students
        self.molds = Mold.objects.filter(institution=institution)

        if self.students.count() == 0:
            messages.error(request, "Nenhum estudante cadastrado!")
            return redirect('anamnesis_list')
        if self.molds.count() == 0:
            messages.error(request, "Nenhum Molde de Questões criado!")
            return redirect('anamnesis_list')

        form = self.get_form(self.get_form_class())

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_form_kwargs(self):
        kwargs = super(AnamnesisCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['student'] = self.students
        kwargs['molds'] = self.molds
        return kwargs


class QuestionList(ListView):
    model = Question
    template_name = 'anamneses/question_list.html'
    
    def get_queryset(self):
        return Question.objects.filter(Q(institution=self.request.user.institution) | Q(institution__id__isnull=True))


class QuestionCreate(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'anamneses/question_create.html'
    success_url = reverse_lazy('question_list')
    success_message = 'Questões criadas com sucesso!'

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
            return self.form_valid(question_form)
        else:
            return self.form_invalid(question_form)
    
    def form_valid(self, question_form):
        questions_instances = question_form.save(commit=False)

        for obj in question_form.deleted_objects:
            obj.delete()

        for question in questions_instances:
            question.institution = self.request.user.institution

        questions = Question.objects.bulk_create(questions_instances)
        self.object = questions[0]

        messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())

class MoldList(ListView):
    model = Mold
    template_name = 'anamneses/mold_list.html'
    
    def get_queryset(self):
        return Mold.objects.filter(Q(institution=self.request.user.institution) | Q(institution__id__isnull=True))


class MoldCreate(SuccessMessageMixin, CreateView):
    model = Mold
    form_class = MoldForm
    template_name = 'anamneses/mold_create.html'
    success_url = reverse_lazy('mold_list')
    success_message = 'Molde criado com sucesso!'

    def get(self, request):
        self.object = None
        self.questions = Question.objects.filter(Q(institution=request.user.institution) | Q(institution__id__isnull=True))

        form = self.get_form(self.get_form_class())

        return self.render_to_response(
            self.get_context_data(
                form=form
            )
        )
    
    def post(self, request):
        self.object = None
        institution = request.user.institution
        self.questions = Question.objects.filter(Q(institution=institution) | Q(institution__id__isnull=True))

        form = self.get_form(self.get_form_class())

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(MoldCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['question_queryset'] = self.questions
        return kwargs
