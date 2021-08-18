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
from .helpers import ajax_login_required
import requests
import logging
import json
import bcrypt


logger = logging.getLogger(__name__)

class Main_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):

        return HttpResponseRedirect(reverse('main:mainImsPage'))
@login_required
def mainImsPage(request):
    template_name = 'main/mainIncl.html'

    return render(request, template_name)

def getMainMenu(request):
    param = json.loads(request.GET['param'])

    # api 호출
    r = requests.get('http://emp_api:5001/getMainMenu', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    logger.info(json.loads(r.text))
    return JsonResponse(r.json(), safe=False)

def getSubMenu(request):
    param = json.loads(request.GET['param'])
    # api 호출
    r = requests.get('http://emp_api:5001/getSubMenu', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    logger.info(json.loads(r.text))
    return JsonResponse(r.json(), safe=False)

def index(request):
    userInfo = str(request.user)
    logger.info('index user')
    logger.info(userInfo)
    auth='';
    if (userInfo is not None) and (userInfo != 'AnonymousUser'):
        # 로그인 정보
        datas = {'emp_id':userInfo}
        r = requests.post('http://emp_api:5001/authSearch', data=datas)
        test= 'user ccc'
        logger.info(json.loads(r.text))
        json_data = json.loads(r.text)
        auth = json_data['auth']
    else :
        test = 'none'
    logger.info(test)
    context = {
        'auth': auth,
    }
    template_name = 'main/index.html'
    return render(request, template_name,context)
@login_required
def sample(request, sample):
    logger.info('>>>>>>>>>>>>>>'+sample)
    template_name = 'sample/' + sample + '.html'

    return render(request, template_name)

@ajax_login_required
def sample_ajax(request):

    param = json.loads(request.GET['param'])

    data = {
        #'email' : param['email'],
        'password' : param['password'],
        'addr' : param['addr'] + ' ' + param['addrDetl'],
        'Check' : param['chk']
    }
    logger.info(data)
    return JsonResponse(data)

def login_form(request):
    template_name = 'main/login.html'
    form = LoginForm()
    logger.info('loginform >>>>>>>>>>>>>>>>>>>')
    try:
        next = request.GET['next']
    except:
        next = '/'

    return render(request, template_name, {'form': form, 'next': next})

def login_form2(request):
    template_name = 'main/login2.html'
    form = LoginForm()
    logger.info('loginform >>>>>>>>>>>>>>>>>>>')
    try:
        next = request.GET['next']
    except:
        next = '/'

    return render(request, template_name, {'form': form, 'next': next})

def signin(request):
    logger.info('data skill >>>>>>>>>>>>>>>>>>>33')
    logger.info(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    #email = request.POST['email']
    next = request.POST['next']
    encPassword = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    logger.info(username)
    logger.info(password)
    logger.info(encPassword)
    datas = {
         'emp_id' : username,
         'emp_pw' : password
    }
    logger.info('data set33333 >>>>>>>>>>>>>>>>>>>')
    user = authenticate(request, username=username, password=encPassword)
    userCheck = User.objects.filter(username=username)

    logger.info(user)
    logger.info(userCheck)
    if user is None:
        logger.info('user fail')
        r = requests.post('http://emp_api:5001/SingIn', data=datas)
        if not userCheck :
            logger.info('usercheck fail')
            user = User.objects.create_user(username=username,  password=encPassword)  #임시 , email=email
            logger.info('fail  >>>>>>>>>>>>>>>>>>>')
    else:
        r = requests.post('http://emp_api:5001/SingIn', data=datas)
        # 사용자 없으면 직원관리 api 호출
        # if 직원정보 있으면:
            # user = User.objects.create_user 직원정보로 사용자 생성
        # else: 직원정보 없으면
            # redirect('/')


    json_data = json.loads(r.text)
    status = json_data['status']
    logger.info('Login result3333333>>>>>>>>>>>>>>>>>>>')
    logger.info(json.loads(r.text))
    logger.info(status)
    if status == 200 :
        logger.info('login yes')
        login(request, user)
        logger.info(next)
        #return HttpResponseRedirect(resolve_url(next))
        #return redirect(next)
        return JsonResponse(r.json())
    else :
        logger.info('login no')
        next = '/main/login'
        return JsonResponse(r.json())

def signin2(request):
    logger.info('data signin dili >>>>>>>>>>>>>>>>>>>')
    logger.info(request.POST)
    username = request.POST['username']
    logger.info(request.POST['username'])
    password = request.POST['password']
    #email = request.POST['email']
    next = request.POST['next']

    datas = {
         'emp_id' : username,
         'emp_pw' : password
    }
    user = authenticate(request, username=username, password=password)
    userCheck = User.objects.filter(username=username)
    logger.info(user)
    logger.info(userCheck)
    if user is None:
        r = requests.post('http://emp_api:5001/SingIn', data=datas)
        if not userCheck:
            logger.info('usercheck fail')
            user = User.objects.create_user(username=username, password=password)  # 임시 , email=email
    else:
        r = requests.post('http://emp_api:5001/SingIn', data=datas)
        # 사용자 없으면 직원관리 api 호출
        # if 직원정보 있으면:
            # user = User.objects.create_user 직원정보로 사용자 생성
        # else: 직원정보 없으면
            # redirect('/')


    json_data = json.loads(r.text)
    status = json_data['status']
    logger.info(json.loads(r.text))
    logger.info(status)
    if status == 200 :
        logger.info('login yes')
        login(request, user)
        logger.info(next)
        return JsonResponse(r.json())
    else :
        logger.info('login no')
        next = '/main/login2'
        return JsonResponse(r.json())

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:mainImsPage'))

# def ajax_login_required(function):
#     def wrap(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return function(request, *args, **kwargs)
#         raise PermissionDenied ## or 401 == not authenticated
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap