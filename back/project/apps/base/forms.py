from django.utils.translation import gettext_lazy as _
from django import forms
from .models import *


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ('owner', 'name', 'address', 'cnpj', 'state', 'city')
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
            'father_age': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Idade do Pai'}
            ),
            'father_profission': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Profissão do Pai'}
            ),
            'father_workplace': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Local de trabalho do Pai'}
            ),
            'is_stepfather': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'mother_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nome da Mãe'}
            ),
            'mother_age': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Idade da Mãe'}
            ),
            'mother_profission': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Profissão da Mãe'}
            ),
            'mother_workplace': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Local de trabalho da Mãe'}
            ),
            'is_stepmother': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }


class StudentForm(forms.ModelForm):
    palliatives_measures = forms.ModelMultipleChoiceField(label=_('Medidas Paliativas'), required=False, queryset=None, 
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'form-check-input'}
        )
    )
    additional_information = forms.ModelMultipleChoiceField(label=_('Informações Adicionais'), required=False, queryset=None, 
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'form-check-input'}
        )
    )
    check_others_measures = forms.BooleanField(label=_('Outras'), required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'onclick': "showOthers('measures')"}
        )
    )
    check_others_informations = forms.BooleanField(label=_('Outras'), required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'onclick': "showOthers('informations')"}
        )
    )
    others_measures = forms.CharField(label=_('Outras medidas'), required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'style': 'height: 200px'}
        )
    )
    others_informations = forms.CharField(label=_('Outras informações'), required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'style': 'height: 200px'}
        )
    )

    class Meta:
        model = Student
        fields = (
            'name', 'birthday', 'gender', 'address','phone', 'name_class', 'sus_number','has_nickname', 'nickname', 
            'who_add_nickname', 'why_add_nickname', 'likes_nickname', 'school_entry_date', 'palliatives_measures', 
            'additional_information', 'check_others_measures', 'check_others_informations', 'others_measures', 
            'others_informations'
        )
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
            'name_class': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Turma'}
            ),
            'sus_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Número do SUS do Aluno'}
            ),
            'has_nickname': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'onchange': 'toggleNickFields()'}
            ),
            'nickname': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Apelido do Aluno'}
            ),
            'who_add_nickname': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Quem deu o apelido ao Aluno'}
            ),
            'why_add_nickname': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Por que deu o apelido ao Aluno'}
            ),
            'likes_nickname': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'school_entry_date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Data de entrada na escola'}
            )
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        palliatives_measures = kwargs.pop('palliatives_measures', None)
        additional_information = kwargs.pop('additional_information', None)

        super(StudentForm, self).__init__(*args, **kwargs)

        if palliatives_measures:
            self.fields['palliatives_measures'].queryset = palliatives_measures
        if additional_information:
            self.fields['additional_information'].queryset = additional_information
    
    def clean(self, *args, **kwargs):
        super(StudentForm, self).clean(*args, **kwargs)

        if self.request:
            self.instance.institution = self.request.user.institution
            self.instance.add_by = self.request.user


class UserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_("Senha"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Senha'}
        )
    )
    password2 = forms.CharField(
        label=_("Confirmar senha"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirmar senha'}
        )
    )

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'full_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nome Completo'}
            ),
            'email': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Email'}
            ),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Telefone'}
            )
        }
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        self.user = request.user
        super(UserForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.institution = self.user.institution
            user.save()

        return user


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


class WeightsForm(forms.ModelForm):
    class Meta:
        model = WeightTrainedModel
        fields = ['weight',]
        widgets = {
            'weight': forms.ClearableFileInput(
                attrs={
                    'multiple': True
                }
            )
        }

class TrainedModelForm(forms.ModelForm):
    weights = forms.FileField(label=_('Pesos do modelo'), required=False, widget=
        forms.ClearableFileInput(
            attrs={
                'multiple': True
            }
        )
    )

    class Meta:
        model = TrainedModel
        fields = ['name', 'model', 'weights', 'observation', 'active']
