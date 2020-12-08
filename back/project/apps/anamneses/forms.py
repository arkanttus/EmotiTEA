from django import forms
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
    questions = forms.ModelChoiceField(required=True, queryset=None, widget=forms.Select(
        attrs={'class': 'form-select'}
    ))

    class Meta:
        model = Mold
        fields = ('description', 'questions')
        widgets = {
            'description': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }
    

    def __init__(self, *args, **kwargs):
        question_queryset = kwargs.pop('question_queryset', None)

        if question_queryset:
            self.fields['questions'].queryset = question_queryset


class AnamnesisForm(forms.ModelForm):
    molds = forms.ModelChoiceField(required=True, queryset=None, widget=forms.Select(
        attrs={'class': 'form-select'}
    ))

    class Meta:
        model = Anamnesis
        fields = ('molds',)
    

    def __init__(self, *args, **kwargs):
        mold_queryset = kwargs.pop('mold_queryset', None)

        if mold_queryset:
            self.fields['molds'].queryset = mold_queryset


QuestionFormSet = forms.formset_factory(QuestionForm, extra=2, can_delete=True)

'''
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content',)
        widgets = {
            'content': forms.
        }
'''

