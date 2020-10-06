from django.conf.urls import url, include
from django.urls import path
from . import views

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

app_name = 'prj_api'

urlpatterns = [
    # url(r'^$', views.Prj_api_index.as_view(), name='prj_api'),
    path('', login_required(views.Prj_api_index.as_view()), name='prj_api'),
    path('index/', login_required(views.Prj_api_index.as_view()), name='prj_api_index'),
    path('retrieve/', views.retrieve, name='retrieve'),

    # 프로젝트 등록
    url(r'^prjReg/', views.prjReg, name='prjReg'),
    url(r'^retrievePrjInfo/get', views.retrievePrjInfo, name='retrievePrjInfo'),
    url(r'^retrieveReqSkil/get', views.retrieveReqSkil, name='retrieveReqSkil'),
    url(r'^retrieveSkilName/', views.retrieveSkilName, name='retrieveSkilName'),
    url(r'^prjSave/post', views.prjSave, name='prjSave'),
    url(r'^prjDelete/post', views.prjDelete, name='prjDelete'),

    # 프로젝트 투입 관리
    url(r'^prjInpuMgmt/', views.prjInpuMgmt, name='prjInpuMgmt'),
    url(r'^prjInpuSearch/get', views.prjInpuSearch, name='prjInpuSearch'),
    url(r'^prjInpuDelete/', views.prjInpuDelete, name='prjInpuDelete'),
    url(r'^prjInpuSave/', views.prjInpuSave, name='prjInpuSave'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)