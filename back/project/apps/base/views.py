from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView
from .models import Photos
from .forms import PhotosForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'base/dashboard.html'


class PhotoCreate(CreateView):
    model = Photos
    form_class = PhotosForm
    template_name = 'base/photo_teste.html'

    def post(self, request):
        form = self.get_form(self.get_form_class())
        files = request.FILES.getlist('path')

        print(files)

