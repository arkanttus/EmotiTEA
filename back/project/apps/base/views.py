from django.shortcuts import render, redirect
from .models import Photos
from .forms import PhotosForm
from django.views.generic import CreateView


class PhotoCreate(CreateView):
    model = Photos
    form_class = PhotosForm
    template_name = 'base/photo_teste.html'

    def post(self, request):
        form = self.get_form(self.get_form_class())
        files = request.FILES.getlist('path')

        print(files)

