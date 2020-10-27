from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'skil_api'

urlpatterns = [
    path('', login_required(views.Skil_api_index.as_view()), name='skil_api'),
    url(r'^$', views.Skil_api_index.as_view(), name='skil_api'),
    url(r'^devReg/', views.devReg, name='devReg'),
    url(r'^prjMgmt/', views.prjMgmt, name='prjMgmt'),

    # mariadb test
    url(r'^maria/', views.maria.as_view(), name='maria'),
    url(r'^getMariaDB/', views.getMariaDB, name='getMariaDB'),

    # 개발자 조회
    url(r'^devMgmt/', views.devMgmt, name='devMgmt'),
    url(r'^devMgmtSearch/get', views.devMgmtSearch, name='devMgmtSearch'),

    # 프리 개발자 등록
    url(r'^retrieveDevInfo/get', views.retrieveDevInfo, name='retrieveDevInfo'),
    url(r'^devSave/post', views.devSave, name='devSave'),
    url(r'^devDelete/post', views.devDelete, name='devDelete'),

    # 스킬관리
    url(r'^skilMgmt/', views.skilMgmt, name='skilMgmt'),
    url(r'^skilMgmtSearch/get', views.skilMgmtSearch, name='skilMgmtSearch'),
    url(r'^skilMgmtDetl/', views.skilMgmtDetl.as_view(), name='skilMgmtDetl'),
    
    # 스킬관리상세팝업
    url(r'^skilRegPopup/', views.skilRegPopup, name='skilRegPopup'),
    url(r'^skilRegPopupSearch/get', views.skilRegPopupSearch, name='skilRegPopupSearch'),
    url(r'^retrieveEmpSkilCd/', views.retrieveEmpSkilCd, name='retrieveEmpSkilCd'),
    url(r'^deleteSkilDetl/post', views.deleteSkilDetl, name='deleteSkilDetl'),
    url(r'^saveSkilDetl/post', views.deleteSkilDetl, name='saveSkilDetl'),

    # 공통 코드 조회
    url(r'^retrieveCmmCd/', views.retrieveCmmCd, name='retrieveCmmCd'),

    # 스킬 코드 관리
    url(r'^skilCdMgmt/', views.skilCdMgmt, name='skilCdMgmt'),
    url(r'^retrieveSkilCd/', views.retrieveSkilCd, name='retrieveSkilCd'),
    url(r'^getSkilCdMgmt/', views.getSkilCdMgmt, name='getSkilCdMgmt'),
    url(r'^deleteSkilCd/', views.deleteSkilCd, name='deleteSkilCd'),
    url(r'^saveSkilCd/', views.saveSkilCd, name='saveSkilCd')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)