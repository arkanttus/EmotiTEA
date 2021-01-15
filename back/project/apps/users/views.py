from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
    PasswordChangeView
)
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import UserForm, AuthenticationForm, UpdatePasswordForm


User = get_user_model()

login_page = 'users/login.html'
register_page = 'users/register.html'

class LoginView(DjangoLoginView):
    template_name = login_page
    form_class = AuthenticationForm
    redirect_authenticated_user = True


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = register_page
    model = User
    form_class = UserForm
    success_message = 'Conta cadastrada com sucesso!'
    success_url = reverse_lazy('login')


'''class UpdatePassword(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UpdatePasswordForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('change_password')
    success_message = 'Senha atualizada com sucesso!'

    def get_object(self):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs = super(UpdatePassword, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs'''


class UpdatePassword(SuccessMessageMixin, PasswordChangeView):
    model = User
    form_class = UpdatePasswordForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('change_password')
    success_message = 'Senha atualizada com sucesso!'

def reset_password(request):
    return render(request, 'users/reset_password.html')