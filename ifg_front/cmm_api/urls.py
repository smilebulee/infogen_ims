from django.conf.urls import url, include
from . import views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

app_name = 'cmm_api'

urlpatterns = [
    path('', views.Cmm_api_index.as_view(), name='cmm_api'),
    path('getCodes/', views.getCodes, name='getCodes'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)