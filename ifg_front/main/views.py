from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views import View
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from urllib.parse import urlparse
from functools import wraps
from django.core.exceptions import PermissionDenied
import requests
import logging
import json

logger = logging.getLogger(__name__)

class Main_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):

        return HttpResponseRedirect(reverse('main:index'))

def index(request):
    template_name = 'main/index.html'
    return render(request, template_name)

@login_required
def sample(request, sample):
    logger.info('>>>>>>>>>>>>>>'+sample)
    template_name = 'sample/' + sample + '.html'

    return render(request, template_name)

@login_required
def sample_ajax(request):

    param = json.loads(request.GET['param'])

    data = {
        'email' : param['email'],
        'password' : param['password'],
        'addr' : param['addr'] + ' ' + param['addrDetl'],
        'Check' : param['chk']
    }
    logger.info(data)
    return JsonResponse(data)

def login_form(request):
    template_name = 'main/login.html'
    form = LoginForm()

    try:
        next = request.GET['next']
    except:
        next = '/'

    return render(request, template_name, {'form': form, 'next': next})

def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    next = request.POST['next']

    user = authenticate(request, username=username, password=password)
    if user is None:
        user = User.objects.create_user(username=username, password=password, email=email)  #임시

        # 사용자 없으면 직원관리 api 호출
        # if 직원정보 있으면:
            # user = User.objects.create_user 직원정보로 사용자 생성
        # else: 직원정보 없으면
            # redirect('/')

    login(request, user)
    return redirect(next)

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))

def ajax_login_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        raise PermissionDenied ## or 401 == not authenticated
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap