"""ifg_front URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main.urls')),
    path('main/', include('main.urls')),

    path('emp/', include('emp_api.urls')),
    path('prj/', include('prj_api.urls')),
    path('skil/', include('skil_api.urls')),
    path('cmm/', include('cmm_api.urls')),
    path('cnc/', include('cnc_api.urls')),
    path('dili/', include('dili_api.urls')),
    path('eval/', include('eval_api.urls')),
    path('kpi/', include('kpi_api.urls')),
    path('stat/', include('stat_api.urls')),
    path('site/', include('site_api.urls')),

]
