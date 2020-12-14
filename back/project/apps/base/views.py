from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, ListView
from .models import Photos, Student, Affiliation
from .forms import PhotosForm, StudentForm, AffiliationForm


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

    def get(self, request):
        self.object = None
        form = self.get_form(self.get_form_class())

        affiliation_form = AffiliationForm()
        photos_form = PhotosForm()


        return self.render_to_response(
            self.get_context_data(
                form=form,
                affiliation_form=affiliation_form,
                photos_form=photos_form
            )
        )



class StudentList(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'base/student_list.html'

    def get_queryset(self):
        return Student.objects.filter(institution=self.request.user.institution)