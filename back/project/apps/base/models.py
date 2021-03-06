import uuid
from datetime import datetime
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .utils import normalize_filename


User = get_user_model()


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
    palliatives_measures = models.ManyToManyField(
        'base.PalliativeMeasure',
        verbose_name=_('Medidas Paliativas'),
        related_name='students',
        blank=True
    )
    additional_information = models.ManyToManyField(
        'base.AdditionalInformation',
        verbose_name=_('Informações Adicionais'),
        related_name='students',
        blank=True
    )
    name = models.CharField(_('Nome'), max_length=100)
    name_class = models.CharField(_('Turma'), max_length=50, default='1A')
    birthday = models.DateField(_('Data de nascimento'), default='16/09/2005')
    gender = models.CharField(_('Gênero'), max_length=1, choices=Gender.choices, default=Gender.FEMALE)
    address = models.CharField(_('Endereço'), max_length=255, default='Rua dos Testadores, Nº 0')
    phone = models.CharField(_('Telefone'), max_length=30, default='(68) 4002-8922')
    sus_number = models.CharField(_('Número do SUS'), max_length=20, default='123')
    has_nickname = models.BooleanField(_('Tem apelido?'), default=False)
    nickname = models.CharField(_('Apelido'), max_length=100, blank=True, null=True)
    who_add_nickname = models.CharField(_('Quem deu o apelido?'), max_length=100, blank=True, null=True)
    why_add_nickname = models.CharField(_('Por que deu o apelido?'), max_length=255, blank=True, null=True)
    likes_nickname = models.BooleanField(_('Gosta do apelido?'), blank=True, null=True)
    school_entry_date = models.DateField(_('Data de entrada na escola'), blank=True, null=True, default='19/06/2009')

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
    father_name = models.CharField(_('Nome do pai'), max_length=100, default='Zezin de Oliveira')
    father_age = models.IntegerField(_('Idade do pai'), default=34)
    father_profission = models.CharField(_('Profissão do pai'), max_length=100, default='Policial')
    father_workplace = models.CharField(_('Local de trabalho do pai'), max_length=255, default='Delegacia')
    is_stepfather = models.BooleanField(_('É padrasto'), default=False, help_text=_('Se for padrasto, marque está opção e preencha os campos referentes ao pai.'))
    mother_name = models.CharField(_('Nome da mãe'), max_length=100, default='Maria de Oliveira')
    mother_age = models.IntegerField(_('Idade da mãe'), default=39)
    mother_profission = models.CharField(_('Profissão da mãe'), max_length=100, default='Manicure')
    mother_workplace = models.CharField(_('Local de trabalho da mãe'), max_length=255, default='Salão de Beleza')
    is_stepmother = models.BooleanField(_('É madrasta'), default=False, help_text=_('Se for madrasta, marque está opção e preencha os campos referentes a mãe.'))

    class Meta:
        verbose_name = _('Filiação')
        verbose_name_plural = _('Filiações')
    
    def __str__(self):
        return f'Filiação de {self.student.name}'


class PalliativeMeasure(BaseModel):
    measure = models.CharField(_('Medida'), max_length=255, help_text=_('Medida paliativa do aluno'))
    specific_student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name=_('Aluno Específico'),
        help_text=_('Se preenchido, essa medida estará disponível apenas para este aluno'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Medida Paliativa')
        verbose_name_plural = _('Medidas Paliativas')
    
    def __str__(self):
        return f'{self.measure}'


class AdditionalInformation(BaseModel):
    information = models.CharField(_('Informação Adicional'), max_length=255, help_text=_('Informação Adicional sobre o aluno'))
    specific_student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name=_('Aluno Específico'),
        help_text=_('Se preenchido, essa informação estará disponível apenas para este aluno'),
        blank=True,
        null=True
    )
    

    class Meta:
        verbose_name = _('Informação Adicional')
        verbose_name_plural = _('Informações Adicionais')
    
    def __str__(self):
        return f'{self.information}'


def path_image(instance, filename):
    titulo_format = normalize_filename(filename)
    return f'photos/{instance.student.pk}/{titulo_format}'

class Photos(BaseModel):
    path = models.ImageField(_('Imagem para treinamento da rede neural'), upload_to=path_image)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name=_('Aluno'),
        related_name='photos'
    )

    class Meta:
        verbose_name = _('Foto Treino')
        verbose_name_plural = _('Fotos Treino')
    

    def __str__(self):
        return f'Imagem de {self.student.name}'


def path_model(instance, filename):
    titulo_format = normalize_filename(filename)
    return f'models/{instance.pk}/{titulo_format}'

class TrainedModel(BaseModel):
    name = models.CharField(_('Nome do modelo'), max_length=100)
    model = models.FileField(_('Modelo treinado'), upload_to=path_model)
    observation = models.CharField(_('Observações'), blank=True, null=True, max_length=255)
    active = models.BooleanField(
        verbose_name=_('Modelo Ativo'), 
        help_text=_('Marque esta opção para que esse modelo seja utilizado. (Qualquer outro modelo ativo será desativado)'),
        default=False
    )

    class Meta:
        verbose_name = _('Modelo Treinado')
        verbose_name_plural = _('Modelos Treinados')
    
    def __str__(self):
        return f'Modelo {self.name}'


def path_weights(instance, filename):
    titulo_format = normalize_filename(filename)
    return f'models/{instance.trained_model.pk}/{titulo_format}'

class WeightTrainedModel(BaseModel):
    trained_model = models.ForeignKey(
        TrainedModel,
        verbose_name=_('Modelo Treinado'),
        on_delete=models.CASCADE,
        related_name='weights'
    )
    weight = models.FileField(_('Arquivo de pesos do modelo'), upload_to=path_weights)

    class Meta:
        verbose_name = _('Arquivo de pesos')
        verbose_name_plural = _('Arquivos de pesos')
    
    def __str__(self):
        return f'Peso de {self.trained_model.name}'
    

