from django.conf.urls import url, include
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    #url(r'^$', views.Main_index.as_view(), name='main'),
    #url(r'^sample/', views.sample, name='sample'),
    path('', views.Main_index.as_view(), name='main'),
    path('index/', views.index, name='index'),
    path('sample/<str:sample>', views.sample, name='sample'),
    path('ajax/get', views.sample_ajax, name='sample_ajax'),
    path('login/', views.login_form, name='login_form'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)