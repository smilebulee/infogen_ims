from django.conf.urls import url, include
from . import views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

app_name = 'cmm_api'

urlpatterns = [
    path('', views.Cmm_api_index.as_view(), name='cmm_api'),
    path('getCodeGrps/', views.getCodeGrps, name='getCodeGrps'),
    path('getCodes/', views.getCodes, name='getCodes'),
    path('codeMng/', views.codeMng, name='codeMng'),
    path('saveGrp/', views.saveGrp, name='saveGrp'),
    path('deleteGrp/', views.deleteGrp, name='deleteGrp'),
    path('saveCd/', views.saveCd, name='saveCd'),
    path('deleteCd/', views.deleteCd, name='deleteCd'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)