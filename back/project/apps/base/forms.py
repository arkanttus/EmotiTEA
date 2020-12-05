from django import forms
from .models import *


class PhotosForm(forms.ModelForm):
    class Meta:
        model = Photos
        fields = ['path',]
        widgets = {
            'path': forms.ClearableFileInput(
                attrs={
                    'multiple': True
                }
            )
        }


'''class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ('owner', 'users', )'''