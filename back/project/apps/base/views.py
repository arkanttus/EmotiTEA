from os import listdir
from os.path import isfile, join
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from .models import *
from .forms import *
from .permissions import *


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'base/dashboard.html'


class PhotoCreate(LoginRequiredMixin, CreateView):
    model = Photos
    form_class = PhotosForm
    template_name = 'base/photo_teste.html'

    def post(self, request):
        form = self.get_form(self.get_form_class())
        files = request.FILES.getlist('path')

        print(files)


class StudentList(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'base/student_list.html'

    def get_queryset(self):
        return Student.objects.filter(institution=self.request.user.institution)


class StudentView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'base/student_view.html'


class StudentCreate(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'base/student_create.html'
    success_url = reverse_lazy('student_list')
    success_message = 'Aluno criado com sucesso!'

    def post(self, request):
        self.object = None
        self.palliatives_measures = PalliativeMeasure.objects.filter(
            specific_student__id__isnull=True
        )
        self.additional_information = AdditionalInformation.objects.filter(
            specific_student__id__isnull=True
        )

        if self.palliatives_measures.count() == 0:
            messages.error(request, "Nenhuma Medida Paliativa criada!")
            return redirect('student_list')
        if self.additional_information.count() == 0:
            messages.error(request, "Nenhuma Informação Adicional criada!")
            return redirect('student_list')

        form = self.get_form(self.get_form_class())

        affiliation_form = AffiliationForm(request.POST)
        photos_form = PhotosForm(request.POST, request.FILES)

        if form.is_valid() and affiliation_form.is_valid() and photos_form.is_valid():
            return self.form_valid(form, affiliation_form, photos_form)
        else:
            return self.form_invalid(form, affiliation_form, photos_form)

    def get(self, request):
        self.object = None
        self.palliatives_measures = PalliativeMeasure.objects.filter(
            specific_student__id__isnull=True
        )
        self.additional_information = AdditionalInformation.objects.filter(
            specific_student__id__isnull=True
        )

        if self.palliatives_measures.count() == 0:
            messages.error(request, "Nenhuma Medida Paliativa criada!")
            return redirect('student_list')
        if self.additional_information.count() == 0:
            messages.error(request, "Nenhuma Informação Adicional criada!")
            return redirect('student_list')

        form = self.get_form(self.get_form_class())

        affiliation_form = AffiliationForm()
        photos_form = PhotosForm()

        palliatives_measures = PalliativeMeasure.objects.all()
        additional_information = AdditionalInformation.objects.all()

        return self.render_to_response(
            self.get_context_data(
                form=form,
                affiliation_form=affiliation_form,
                photos_form=photos_form,
                palliatives_measures=palliatives_measures,
                additional_information=additional_information
            )
        )

    def form_valid(self, form, affiliation_form, photos_form):
        user = self.request.user

        self.object = student = form.save()

        if form.cleaned_data['check_others_measures'] :
            student.palliatives_measures.create(measure=form.cleaned_data['others_measures'], specific_student=student)
        if form.cleaned_data['check_others_informations'] :
            student.additional_information.create(information=form.cleaned_data['others_informations'], specific_student=student)

        affiliation = affiliation_form.save(commit=False)
        affiliation.student = student
        affiliation.save()

        files = self.request.FILES.getlist('path')
        files_instance = [ Photos(path=file, student=student) for file in files]
        Photos.objects.bulk_create(files_instance)

        messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())

    def form_invalid(self, form, affiliation_form, photos_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                affiliation_form=affiliation_form,
                photos_form=photos_form
            )
        )

    def get_form_kwargs(self):
        kwargs = super(StudentCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['palliatives_measures'] = self.palliatives_measures
        kwargs['additional_information'] = self.additional_information
        return kwargs


class MonitoringView(ListView):
    model = Student
    template_name = 'base/monitoring.html'

    def get_queryset(self):
        return Student.objects.filter(institution=self.request.user.institution)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = [f for f in listdir('static/videos') if isfile(join('static/videos', f))]
        return context


class MonitoringIndividual(CanHandleStudent, DetailView):
    model = Student
    template_name = 'base/monitoring_individual.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trained_model = self.get_trained_model()

        if not trained_model:
            raise TrainedModel.DoesNotExist

        context['model'] = trained_model
        context['me'] = self.request.GET.get('me') == 'true'

        return context

    def get_trained_model(self):
        trained_model = TrainedModel.objects.filter(active=True).first()
        if trained_model:
            return trained_model.model


class UserList(LoginRequiredMixin, IsInstitutionOwner, ListView):
    model = User
    template_name = 'base/user_list.html'

    def get_queryset(self):
        return User.objects.filter(institution=self.request.user.institution).exclude(id=self.request.user.id)


class UserCreate(LoginRequiredMixin, IsInstitutionOwner, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'base/user_create.html'
    success_url = reverse_lazy('user_list')
    success_message = 'Usuário criado com sucesso!'

    def get_form_kwargs(self):
        kwargs = super(UserCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs