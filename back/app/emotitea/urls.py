from django.contrib import admin
from django.conf.urls.static import static, settings
from django.urls import path
from users.views import LoginView, RegisterView

from .settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
