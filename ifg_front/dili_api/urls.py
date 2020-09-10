from django.conf.urls import url, include
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'dili_api'

urlpatterns = [
    url(r'^$', views.Dili_api_index.as_view(), name='dili_api'),

    #mariadb 연결 샘플
    url(r'^mariatest/', views.mariatest.as_view(), name='mariatest'),
    url(r'^getMaria/', views.getMaria, name='getMaria'),
    url(r'^getWrkTimeInfoByEml/', views.getWrkTimeInfoByEml, name='getWrkTimeInfoByEml'),
    url(r'^getYryMgmt/', views.getYryMgmt, name='getYryMgmt'),
    url(r'^scheduleMgmt/', views.scheduleMgmt.as_view(), name='scheduleMgmt'),
    url(r'^wrkApvlReq/', views.wrkApvlReq.as_view(), name='wrkApvlReq'),
    url(r'^yryApvlReq/', views.yryApvlReq.as_view(), name='yryApvlReq'),
    url(r'^noticeLst/', views.noticeLst.as_view(), name='noticeLst'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)