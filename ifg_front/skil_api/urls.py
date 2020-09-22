from django.conf.urls import url, include
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'skil_api'

urlpatterns = [
    url(r'^$', views.Skil_api_index.as_view(), name='skil_api'),
    url(r'^devEnrl/', views.devEnrl, name='devEnrl'),
    url(r'^prjMgmt/', views.prjMgmt, name='prjMgmt'),

    # mariadb test
    url(r'^maria/', views.maria.as_view(), name='maria'),
    url(r'^getMariaDB/', views.getMariaDB, name='getMariaDB'),

    # 개발자 등록
    url(r'^devSave/post', views.devSave, name='devSave'),
    url(r'^devDelete/post', views.devDelete, name='devDelete'),

    # 프로젝트 등록
    url(r'^prjSave/post', views.prjSave, name='prjSave'),
    url(r'^prjDelete/post', views.prjDelete, name='prjDelete'),
    url(r'^reqSkilSave/post', views.reqSkilSave, name='reqSkilSave'),

    # 프로젝트 투입 관리
    url(r'^prjInpuMgmt/', views.prjInpuMgmt, name='prjInpuMgmt'),
    url(r'^prjInpuSearch/get', views.prjInpuSearch, name='prjInpuSearch'),
    url(r'^prjInpuDelete/', views.prjInpuDelete, name='prjInpuDelete'),

    # 스킬관리
    url(r'^skilMgmt/', views.skilMgmt, name='skilMgmt'),
    url(r'^skilMgmtSearch/get', views.skilMgmtSearch, name='skilMgmtSearch'),
    url(r'^skilMgmtDetl/', views.skilMgmtDetl.as_view(), name='skilMgmtDetl'),
    
    # 스킬관리상세팝업
    url(r'^skilRegPopup/', views.skilRegPopup, name='skilRegPopup'),
    url(r'^skilRegPopupSearch/', views.skilRegPopupSearch, name='skilRegPopupSearch'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)