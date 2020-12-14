import uuid
from datetime import datetime
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .utils import normalize_filename


User = get_user_model()


class TrueFalse(models.TextChoices):
    NO = 'NAO', _('Não')
    YES = 'SIM', _('Sim')


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Última atualização'), editable=False, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.created_at:
            self.updated_at = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)


class Institution(BaseModel):
    owner = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Criador'),
        help_text=_('Criador desta instituição.'),
        related_name='my_institution',
        null=True
    )
    name = models.CharField(_('Nome'), max_length=100)
    address = models.CharField(_('Endereço'), max_length=255, null=True, blank=True)
    cnpj = models.CharField(_('CNPJ'), max_length=18, null=True, blank=True)
    state = models.CharField(_('Estado'), max_length=100, null=True, blank=True)
    city = models.CharField(_('Cidade'), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _('Instituição')
        verbose_name_plural = _('Instituições')
    

    def __str__(self):
        return f'{self.name}'


class Student(BaseModel):
    
    class Gender(models.TextChoices):
        FEMALE = 'F', _('Feminino')
        MALE = 'M', _('Masculino')


    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        verbose_name=_('Instituição'),
        related_name='students'
    )
    add_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Adicionado por'),
        related_name='students'
    )
    name = models.CharField(_('Nome'), max_length=100)
    name_class = models.CharField(_('Turma'), max_length=50)
    birthday = models.DateField(_('Data de nascimento'))
    gender = models.CharField(_('Gênero'), max_length=1, choices=Gender.choices, default=Gender.FEMALE)
    address = models.CharField(_('Endereço'), max_length=255)
    phone = models.CharField(_('Telefone'), max_length=30)
    sus_number = models.CharField(_('Número do SUS'), max_length=20)
    has_nickname = models.BooleanField(_('Tem apelido?'), default=False)
    nickname = models.CharField(_('Apelido'), max_length=100, blank=True, null=True)
    who_add_nickname = models.CharField(_('Quem deu o apelido?'), max_length=100, blank=True, null=True)
    why_add_nickname = models.CharField(_('Por que deu o apelido?'), max_length=255, blank=True, null=True)
    likes_nickname = models.BooleanField(_('Gosta do apelido?'), blank=True, null=True)
    school_entry_date = models.DateField(_('Data de entrada na escola'))

    class Meta:
        verbose_name = _('Aluno')
        verbose_name_plural = _('Alunos')
    

    def __str__(self):
        return f'{self.name}'


class Affiliation(BaseModel):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        verbose_name=_('Aluno'),
        related_name='affiliation'
    )
    father_name = models.CharField(_('Nome do pai'), max_length=100)
    father_age = models.IntegerField(_('Idade do pai'))
    father_profission = models.CharField(_('Profissão do pai'), max_length=100)
    father_workplace = models.CharField(_('Local de trabalho do pai'), max_length=255)
    is_stepfather = models.BooleanField(_('É padrasto'), default=False)
    mother_name = models.CharField(_('Nome da mãe'), max_length=100)
    mother_age = models.IntegerField(_('Idade da mãe'))
    mother_profission = models.CharField(_('Profissão da mãe'), max_length=100)
    mother_workplace = models.CharField(_('Local de trabalho da mãe'), max_length=255)
    is_stepmother = models.BooleanField(_('É madrasta'), default=False)

    class Meta:
        verbose_name = _('Filiação')
        verbose_name_plural = _('Filiações')
    

    def __str__(self):
        return f'Filiação de {self.student.name}'


def path_image(instance, filename):
    titulo_format = normalize_filename(filename)
    return f'musics/{instance.pk}/{titulo_format}'

class Photos(BaseModel):
    path = models.ImageField(_('Imagem para treinamento da rede neural'), upload_to=path_image)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name=_('Aluno')
    )

    class Meta:
        verbose_name = _('Foto Treino')
        verbose_name_plural = _('Fotos Treino')
    

    def __str__(self):
        return f'Imagem de {self.student.name}'
    

