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
    #회원가입 연습추가
    url(r'^testFox2/', views.Emp_api_testFox2.as_view(), name='emp_foxTest2'),
    url(r'^newSearch_ajax/get', views.newSearch_ajax, name='newSearch_ajax'),
    url(r'^idCheck/get', views.idCheck, name='idCheck'),
    #신규 폼 연습
    url(r'^testPark/', views.Emp_api_testPark.as_view(), name='emp_testPark'),
    url(r'^insert_ajax_new/post', views.insert_ajax_new, name='insert_ajax_new'),
    url(r'^newSearch/get', views.newSearch, name='newSearch'),
    #직원조회
    url(r'^empReference/', views.empReference, name='empReference'),
    url(r'^getPage/', views.getPage, name='getPage'),

    #mariadb 연결 샘플
    #mariadb test
    url(r'^mariatest/', views.mariatest.as_view(), name='mariatest'),
    url(r'^getMaria/', views.getMaria, name='getMaria'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)