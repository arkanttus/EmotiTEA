from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
)
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import UserForm, AuthenticationForm


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

    '''def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            print(form.cleaned_data)'''

def reset_password(request):
    return render(request, 'users/reset_password.html')