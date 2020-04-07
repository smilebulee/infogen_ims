from django.conf.urls import url, include
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'emp_api'

urlpatterns = [
    url(r'^$', views.Emp_api_index.as_view(), name='emp_api'),
    url(r'^testFox/', views.Emp_api_testFox.as_view(), name='emp_foxTest'),
    url(r'^insert_ajax/post', views.insert_ajax, name='insert_ajax'),
    url(r'^update_ajax/post', views.update_ajax, name='update_ajax'),
    url(r'^search_ajax/get', views.search_ajax, name='search_ajax'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)