from django import forms
from .models import *


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ('owner', 'users', 'name', 'address', 'cnpj', 'state', 'city')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nome da Instituição'}
            ),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Endereço'}
            ),
            'cnpj': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'CNPJ'}
            ),
            'state': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Estado'}
            ),
            'city': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Cidade'}
            )
        }


class AffiliationForm(forms.ModelForm):
    class Meta:
        model = Affiliation
        fields = ('father_name', 'father_age', 'father_profission',
        'father_workplace', 'is_stepfather', 'mother_name', 'mother_age',
        'mother_profission', 'mother_workplace', 'is_stepmother')
        widgets = {
            'father_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nome do Pai'}
            ),
            'father_age': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Idade do Pai'}
            ),
            'father_profission': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Profissão do Pai'}
            ),
            'father_workplace': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Local de trabalho do Pai'}
            ),
            # 'is_stepfather': forms.BooleanField(
            #     attrs={'class': 'form-control'}
            # ),
            'mother_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nome da Mãe'}
            ),
            # 'mother_age': forms.IntegerField(
            #     attrs={'class': 'form-control', 'placeholder': 'Idade da Mãe'}
            # ),
            'mother_profission': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Profissão da Mãe'}
            ),
            'mother_workplace': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Local de trabalho da Mãe'}
            ),
            # 'is_stepmother': forms.BooleanField(
            #     attrs={'class': 'form-control'}
            # )
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('name', 'birthday', 'gender', 'address','phone', 'sus_number','has_nickname',
        'nickname', 'who_add_nickname', 'why_add_nickname', 'likes_nickname', 'school_entry_date')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nome do Aluno'}
            ),
            'birthday': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Data de aniversário do Aluno'}
            ),
            'gender': forms.Select(
                attrs={'class': 'form-select', 'placeholder': 'Gênero do Aluno'}
            ),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Endereço do Aluno'}
            ),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Telefone do Aluno'}
            ),
            'sus_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Número do SUS do Aluno'}
            ),
            # 'has_nickname': forms.BooleanField(
            #     attrs={'class': 'form-control'}
            # ),
            'nickname': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Apelido do Aluno'}
            ),
            'who_add_nickname': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Quem deu o apelido ao Aluno'}
            ),
            'why_add_nickname': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Por que deu o apelido ao Aluno'}
            ),
            # 'likes_nickname': forms.BooleanField(
            #     attrs={'class': 'form-control'}
            # ),
            'school_entry_date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Data de entrada na escola'}
            )
        }


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

