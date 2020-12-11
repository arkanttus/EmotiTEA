from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from datetime import datetime
from .managers import UserManager


def date_next_form():
    return timezone.now().date() + timezone.timedelta(days=7)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('Email'),
        unique=True,
        error_messages={'unique': _("Já existe um usuário com este email")},
    )
    full_name = models.CharField(_('Nome Completo'), max_length=255)
    phone = models.CharField(_('Número de celular'), max_length=20, blank=True, null=True)
    institution = models.ForeignKey(
        'base.Institution',
        on_delete=models.CASCADE,
        verbose_name=_('Instituição'),
        help_text=_('Instituição que o usuário faz parte'),
        blank=True,
        related_name='users'
    )
    is_staff = models.BooleanField(_('Membro da Equipe'), default=False)
    is_active = models.BooleanField(
        _('Ativo'), default=True, help_text=_('Desative para tirar o acesso do usuário')
    )
    date_joined = models.DateTimeField(_('Criação da Conta'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def __str__(self):
        return f'{self.full_name[:30]}'

