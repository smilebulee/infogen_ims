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
    url(r'^getNoticeLst/', views.getNoticeLst, name='getNoticeLst'),
    url(r'^noticeDtl/', views.noticeDtl.as_view(), name='noticeDtl'),
    url(r'^getWrkApvlReq/', views.getWrkApvlReq, name='getWrkApvlReq'),
    url(r'^saveApvlReq/post', views.saveApvlReq, name='saveApvlReq'),
    url(r'^apvlReqHist/', views.apvlReqHist.as_view(), name='apvlReqHist'),
    url(r'^getApvlReqHist/', views.getApvlReqHist, name='getApvlReqHist'),
    url(r'^empMgmt/', views.empMgmt.as_view(), name='empMgmt'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)