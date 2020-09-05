from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views import generic
from django.http import JsonResponse

from django.core.paginator import Paginator
#from .models import Tb_page

from django.views.decorators.csrf import csrf_exempt
# from .models import TB_EMP,Cd

import requests
import logging
import json

logger = logging.getLogger(__name__)

class Emp_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'emp/index.html'

        r = requests.get('http://emp_api:5001/hello')
        rr = {
            "result":r.text
        }
        
        return render(request, template_name, rr)


class Emp_api_testFox(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'emp/testFox.html'

        r = requests.get('http://emp_api:5001/hello')
        rr = {
            "result": r.text
        }

        return render(request, template_name, rr)

@csrf_exempt
def insert_ajax(request):

    param = json.loads(request.POST['param'])
    logger.info(param)
    datas = {
        'email' : param['email'],
        'password' : param['password'],
        'addr' : param['state'] + ' ' + param['city'] + ' ' + param['addr'] + ' ' + param['addrDetl'] + param['zip'],
        'sex' : param['chk']

    }
    logger.info('request.post : ' + request.POST['param'])
    logger.info(datas)
    #r = requests.post('http://emp_api:5000/save',data=json.dumps(datas))
    r = requests.post('http://emp_api:5001/save', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

@csrf_exempt
def update_ajax(request):

    param = json.loads(request.POST['param'])
    logger.info(param)
    # datas = {
    #     'email' : param['email'],
    #     'password' : param['password'],
    #     'addr' : param['addr'],
    #     'sex' : param['sex']
    # }
    logger.info('request.post : ' + request.POST['param'])
    # logger.info(datas)
    r = requests.post('http://emp_api:5001/update', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

def search_ajax(request):

    param = json.loads(request.GET['param'])

    datas = {
        'email' : param['searchemail']
    }
    logger.info(datas)
    r = requests.get('http://emp_api:5001/search', params=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")
    logger.info(r.json())
    logger.info(json.loads(r.text))
    # return JsonResponse(r.json())
    return JsonResponse(r.json(), safe=False)

## 신규 추가 
class Emp_api_testFox2(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'emp/testFox2.html'

        r = requests.get('http://emp_api:5001/hello')
        rr = {
            "result": r.text
        }

        return render(request, template_name, rr)
## 서치 이메일 or 아이디 검색으로 그리드 호출
def newSearch_ajax(request) :
    logger.info(request)
    param = json.loads(request.GET['param'])
    logger.info("new Search Test")
    datas = {
        'email': param['searchemail']
    }
    logger.info(datas)
    r = requests.get('http://emp_api:5001/search', params=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")
    logger.info(r.json())
    logger.info(json.loads(r.text))
    # return JsonResponse(r.json())
    return JsonResponse(r.json(), safe=False)

def idCheck(request) :
    logger.info("IDCHECK")
    logger.info(request)

    data2 = request.GET['id1']
    datatest = {
        'id' : data2
    }
    logger.info("data??")
    logger.info(datatest)
    logger.info(data2)

    #logger.info('request.post : ' + request.POST['param'])
    # logger.info(datas)
    r = requests.get('http://emp_api:5001/idChektest', params=datatest)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

## 신규 추가
class Emp_api_testPark(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'emp/testPark.html'

        r = requests.get('http://emp_api:5001/hello')
        rr = {
            "result": r.text
        }

        return render(request, template_name, rr)

@csrf_exempt
def insert_ajax_new(request):

    param = json.loads(request.POST['param'])

    datas = {
        'id' : param['id1'],
        'email' : param['email'],
        'password' : param['password'],
        'phone' : param['phone']

    }
    logger.info('request.post : ' + request.POST['param'])
    logger.info(datas)
    r = requests.post('http://emp_api:5001/signUp', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

def newSearch(request) :
    logger.info(request)
    param = json.loads(request.GET['param'])
    logger.info("new Search Test")
    datas = {
        'id' : param['inputId'],
        'email': param['searchemail'],
        'password' :  param['inputSearchPw']
    }
    logger.info(datas)
    r = requests.get('http://emp_api:5001/search2', params=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")
    logger.info(r.json())
    logger.info(json.loads(r.text))
    # return JsonResponse(r.json())
    return JsonResponse(r.json(), safe=False)

def empReference(request):
    template_name = 'emp/empReference.html'

    return render(request, template_name)

def getPage(request) :
    # init data (
    param = json.loads(request.GET['param'])
    logger.info("new Search Test333333")
    datas = {
        'id': param['page'],
    }
    logger.info(datas)
    # 공통 코드마스터 데이터 조회
    #06.23 test 다른 모델 장고 접속확인
    qs = Tb_page.objects.all().order_by('page_id').values('page_id','page_nm','job_dv','remark')
    logger.info(list(qs))
    r = requests.get('http://emp_api:5001/empReferenceInit', params=datas)
    paginator = Paginator(r.json(), 10)
    logger.info("----------------")
    logger.info(paginator)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")

    result = paginator.get_page(param['page'])
    logger.info(list(result.object_list))

    logger.info(result)
    data = {
        'list': list(result.object_list),
        'total_records': paginator.count,
        'total_pages': paginator.num_pages,
        'page': result.number,
        'has_next': result.has_next(),
        'has_prev': result.has_previous()
    }
    logger.info(data)
    logger.info("dadadadaata")

    #logger.info(r.json())
    #logger.info(json.loads(r.text))
    # return JsonResponse(r.json())
    return JsonResponse(data)

class mariatest(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'emp/mariatest.html'

        r = requests.get('http://emp_api:5001/hello')
        rr = {
            "result": r.text
        }

        return render(request, template_name, rr)

def getMaria(request):
    param = json.loads(request.GET['param'])

    #
    r = requests.get('http://emp_api:5001/mariatestDB')
    logger.info("r log")
    logger.info(r)
    logger.info("r.text log")
    logger.info(r.text)
    logger.info("r.json log")
    logger.info(r.json())
    logger.info("json.loads log")
    logger.info(json.loads(r.text))
    return JsonResponse(r.json(), safe=False)