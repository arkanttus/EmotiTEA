from django.contrib import admin
from django.conf.urls.static import static, settings
from django.urls import path
from apps.users.views import LoginView, RegisterView
from apps.users import views as uv
from apps.base.views import PhotoCreate
from apps.anamneses.views import QuestionCreate, MoldCreate

from .settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('question/', QuestionCreate.as_view(), name='question_create'),
    path('mold/', MoldCreate.as_view(), name='mold_create'),
    path('reset_password/', uv.reset_password, name='reset_password'),
    path('', PhotoCreate.as_view(), name='upload'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
