import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseModel


class Question(BaseModel):

    class Types(models.TextChoices):
        TEXT = 'TEXT', _('Texto')
        MULTIPLE_CHOICE = 'MULTI_CHOICE', _('Múltipla Escolha')
        CHECKBOXES = 'CHECKBOXES', _('Caixas de Seleção')
        TRUE_FALSE = 'TRUE_FALSE', _('Verdadeiro ou Falso')

    institution = models.ForeignKey(
        'base.Institution',
        verbose_name=_('Instituição'),
        related_name='questions',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    description = models.CharField(_('Descrição'), max_length=255)
    type = models.CharField(_('Tipo de pergunta'), max_length=12, choices=Types.choices, default=Types.TEXT)
    default_value = models.CharField(_('Valor Padrão'), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _('Questão')
        verbose_name_plural = _('Questões')
    

    def __str__(self):
        return f'{self.description}'
    
    def create_answers(self, type_question):
        pass
        #if type_question == self.Types.TEXT
    
    def serialize_alternatives(self, alternatives):
        return ';'.join(alternatives)

    def deserialize_alternatives(self):
        alternatives = self.default_value
        if alternatives:
            return alternatives.split(';')


class Mold(BaseModel):
    institution = models.ForeignKey(
        'base.Institution',
        verbose_name=_('Instituição'),
        related_name='molds',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(_('Ativo'), default=True)
    title = models.CharField(_('Título'), max_length=255)
    questions = models.ManyToManyField(
        Question,
        verbose_name=_('Questões')
    )

    class Meta:
        verbose_name = _('Molde')
        verbose_name_plural = _('Moldes')
    

    def __str__(self):
        return f'{self.title}'


class Anamnesis(BaseModel):
    is_active = models.BooleanField(_('Ativo'), default=True)
    mold = models.ForeignKey(
        Mold,
        verbose_name=_('Molde'),
        on_delete=models.CASCADE
    )
    institution = models.ForeignKey(
        'base.Institution',
        verbose_name=_('Instituição'),
        related_name='anamneses',
        on_delete=models.CASCADE,
        blank=True
    )
    student = models.ForeignKey(
        'base.Student',
        verbose_name=_('Aluno'),
        on_delete=models.CASCADE,
        related_name='anamneses'
    )

    class Meta:
        verbose_name = _('Anamnese')
        verbose_name_plural = _('Anamneses')
    

    def __str__(self):
        return f'Anamnese de {self.student.name}'


class Answer(BaseModel):
    content = models.CharField(_('Resposta'), max_length=255)
    anamnese = models.ForeignKey(
        Anamnesis,
        verbose_name=_('Anamnese'),
        related_name='answers',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        verbose_name=_('Questão'),
        related_name='answers',
        on_delete=models.CASCADE
    )


    class Meta:
        verbose_name = _('Resposta')
        verbose_name_plural = _('Respostas')
    

    def __str__(self):
        return f'{self.content}'

