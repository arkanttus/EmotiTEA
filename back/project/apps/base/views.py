from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, ListView
from .models import Photos, Student
from .forms import PhotosForm, StudentForm


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


class StudentCreate(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'base/student_create.html'


class StudentList(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'base/student_list.html'

    def get_queryset(self):
        return Student.objects.filter(institution=self.request.user.institution)