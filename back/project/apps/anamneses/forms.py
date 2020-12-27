from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('description', 'type', 'default_value')
        widgets = {
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Descrição'}
            ),
            'type': forms.Select(
                attrs={'class': 'form-select', 'placeholder': 'Tipo da pergunta', 'onchange': "handleTypeQuestion(this)"}
            ),
            'default_value': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Resposta Padrão'}
            )
        }


class MoldForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(label=_('Questões'), required=True, queryset=None, 
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'form-check-input'}
        )
    )

    class Meta:
        model = Mold
        fields = ('title', 'questions')
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Título'}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        question_queryset = kwargs.pop('question_queryset', None)

        super(MoldForm, self).__init__(*args, **kwargs)

        if question_queryset:
            self.fields['questions'].queryset = question_queryset

    def clean(self, *args, **kwargs):
        super(MoldForm, self).clean(*args, **kwargs)

        if self.request:
            self.instance.institution = self.request.user.institution

class AnamnesisForm(forms.ModelForm):
    student = forms.ModelChoiceField(label='Aluno', required=True, queryset=None, widget=forms.Select(
        attrs={'class': 'form-select'}
    ))
    mold = forms.ModelChoiceField(label='Molde', required=True, queryset=None, widget=forms.Select(
        attrs={'class': 'form-select', 'onchange': 'handleMold(this)'}
    ))

    class Meta:
        model = Anamnesis
        fields = ('student', 'mold',)
    

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        student_queryset = kwargs.pop('student', None)
        molds_queryset = kwargs.pop('mold', None)
        initial_mold = kwargs.pop('initial_mold', None)

        super(AnamnesisForm, self).__init__(*args, **kwargs)

        if student_queryset:
            self.fields['student'].queryset = student_queryset
        if molds_queryset:
            self.fields['mold'].queryset = molds_queryset
        if initial_mold:
            self.fields['mold'].initial = initial_mold
    
    def clean(self, *args, **kwargs):
        super(AnamnesisForm, self).clean(*args, **kwargs)

        if self.request:
            self.instance.institution = self.request.user.institution


QuestionFormSet = forms.modelformset_factory(Question, QuestionForm, extra=2, can_delete=True)

'''
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content',)
        widgets = {
            'content': forms.
        }
'''

