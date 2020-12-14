from django.contrib import admin
from django.conf.urls.static import static, settings
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from apps.users import urls as user_urls
from apps.base import urls as base_urls
from apps.anamneses import urls as anamneses_urls
from apps.base.views import IndexView
from .settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('', IndexView.as_view(), name='dashboard'),

    path('', include(user_urls)),
    path('', include(base_urls)),
    path('', include(anamneses_urls)),
    path('admin/', admin.site.urls),

] + static(MEDIA_URL, document_root=MEDIA_ROOT)
