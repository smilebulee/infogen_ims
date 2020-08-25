from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from . import views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

app_name = 'cnc_api'

urlpatterns = [
    path('', login_required(views.Cnc_api_index.as_view()), name='cnc_api'),
    path('test2/', views.test2, name='test2'),
    path('getTestview/', views.getTestview, name='getTestview'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)