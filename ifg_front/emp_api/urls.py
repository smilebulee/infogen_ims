from django.conf.urls import url, include
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'emp_api'

urlpatterns = [
    url(r'^$', views.Emp_api_index.as_view(), name='emp_api'),
    url(r'^testFox/', views.Emp_api_testFox.as_view(), name='emp_foxTest'),
    url(r'^testFox_ajax/get', views.testFox_ajax, name='testFox_ajax'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)