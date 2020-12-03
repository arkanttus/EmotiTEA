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

    description = models.CharField(_('Descrição'), max_length=255)
    type = models.CharField(_('Tipo de pergunta'), max_length=12, choices=Types.choices, default=Types.TEXT)
    #default_value = models.CharField(_(''))

    class Meta:
        verbose_name = _('Questão')
        verbose_name_plural = _('Questões')
    

    def __str__(self):
        return f'{self.description}'


class Mold(BaseModel):
    is_active = models.BooleanField(_('Ativo'), default=True)
    description = models.CharField(_('Descrição'), max_length=255, blank=True, null=True)
    questions = models.ManyToManyField(
        Question,
        verbose_name=_('Questões')
    )

    class Meta:
        verbose_name = _('Molde')
        verbose_name_plural = _('Moldes')
    

    def __str__(self):
        return f'{self.description}'


class Anamnesis(BaseModel):
    is_active = models.BooleanField(_('Ativo'), default=True)
    mold = models.ForeignKey(
        Mold,
        verbose_name=_('Molde'),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Anamnese')
        verbose_name_plural = _('Anamneses')
    

    def __str__(self):
        return f'{self.name}'



class Alternative(BaseModel):
    content = models.CharField(_('Conteúdo'), max_length=100)
    question = models.ForeignKey(
        Question,
        verbose_name=_('Questão associada'),
        related_name='alternatives',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Alternativa')
        verbose_name_plural = _('Alternativas')
    

    def __str__(self):
        return f'{self.content}'


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
    alternative = models.ForeignKey(
        Alternative,
        verbose_name=_('Alternativa'),
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Resposta')
        verbose_name_plural = _('Respostas')
    

    def __str__(self):
        return f'{self.content}'

