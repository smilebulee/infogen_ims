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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)