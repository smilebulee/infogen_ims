from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views import generic
from django.http import JsonResponse
from django.core.paginator import Paginator
#from .models import Tb_page

from django.contrib.auth.decorators import login_required
from main.helpers import ajax_login_required

from django.views.decorators.csrf import csrf_exempt

import requests
import logging
import json

logger = logging.getLogger(__name__)

class Skil_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'skil/index.html'
        r = requests.get('http://skil_api:5003/hello')
        rr = {
            "result": r.text
        }

        return render(request, template_name, rr)

def devReg(request):
    template_name = 'skil/devReg.html'

    return render(request, template_name)

def prjMgmt(request):
    template_name = 'skil/prjMgmt.html'

    return render(request, template_name)

class maria(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'skil/maria.html'
        logger.info("api end")
        r = requests.get('http://skil_api:5003/hello')
        rr = {
            "result": r.text
        }

        return render(request, template_name, rr)

def getMariaDB(request):
    param = json.loads(request.GET['param'])

    logger.info('api start')
    r = requests.get('http://skil_api:5003/mariaClass')
    logger.info("api end")
    logger.info("r log")
    logger.info(r)
    logger.info("r.text log")
    logger.info(r.text)
    logger.info("r.json log")
    logger.info(r.json())
    logger.info("json.loads log")
    logger.info(json.loads(r.text))
    return JsonResponse(r.json(), safe=False)

@ajax_login_required
def devMgmt(request):
    template_name = 'skil/devMgmt.html'

    return render(request, template_name)

def devMgmtSearch(request):

    param = json.loads(request.GET['param'])
    logger.info("devMgmtSearch : skil/views.py")
    datas = {
        'devpBlco': param['devpBlco'],
        'empName': param['empName'],
        'devpDivsCd': param['devpDivsCd']
    }

    logger.info(datas)
    r = requests.get('http://skil_api:5003/devMgmtSearch', params=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")
    logger.info(r.json())
    logger.info(json.loads(r.text))
    # return JsonResponse(r.json())
    return JsonResponse(r.json(), safe=False)

def retrieveDevInfo(request):
    param = json.loads(request.GET['param'])
    logger.info(param)

    params = {
        'emp_no': param['emp_no'],
    }

    r = requests.get('http://skil_api:5003/retrieveDevInfo', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

@ajax_login_required
def devSave(request):
    userId = str(request.user)
    param = json.loads(request.POST['param'])

    datas = {
        'userId': userId
    }

    for row in param:
        datas.setdefault(row, param[row])
    logger.info(datas)
    r = requests.post('http://skil_api:5003/devSave', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

@ajax_login_required
def devDelete(request):
    param = json.loads(request.POST['param'])

    datas = {
    }

    for row in param:
        datas.setdefault(row, param[row])

    r = requests.post('http://skil_api:5003/devDelete', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json())

def skilMgmt(request):
    template_name = 'skil/skilMgmt.html'

    return render(request, template_name)

def skilRegPopup(request):
    template_name = 'skil/skilRegPopup.html'

    return render(request, template_name)

#스킬 코드 관리 화면 호출
def skilCdMgmt(request):
    template_name = 'skil/skilCdMgmt.html'

    return render(request, template_name)

def skilRegPopupSearch(request):

    param = json.loads(request.GET['param'])
    logger.info("skilRegPopup : skil/views.py")
    datas = {
        'cntcDivsCd': param['cntcDivsCd'],
        'empNo': param['empNo'],
    }

    logger.info(datas)
    r = requests.get('http://skil_api:5003/skilRegPopupSearch', params=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")
    logger.info(r.json())
    logger.info(json.loads(r.text))
    # return JsonResponse(r.json())
    return JsonResponse(r.json(), safe=False)

def skilMgmtSearch(request):

    param = json.loads(request.GET['param'])
    logger.info("skilMgmtSearch : skil/views.py")
    logger.info(param)

    datas = {
        'dept': param['dept'],
        'name': param['name'],
        'division': param['division'],
        'skilKind': param['skilKind'],
        'skil': param['skil']
    }

    logger.info(datas)
    r = requests.get('http://skil_api:5003/skilMgmtSearch', params=datas)
    paginator = Paginator(r.json(), 9)
    logger.info("----------------")
    logger.info(paginator)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")

    result = paginator.get_page(param['page'])

    logger.info(result)
    data = {
        'list': list(result.object_list),
        'total_records': paginator.count,
        'total_pages': paginator.num_pages,
        'page': result.number,
        'has_next': result.has_next(),
        'has_prev': result.has_previous()
    }
    # return JsonResponse(r.json())
    return JsonResponse(data)

class skilMgmtDetl(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'skil/skilMgmtDetl.html'
        logger.info("skilMgmtDetl : skil/views.py")
        #화면 호출
        r = requests.get('http://skil_api:5003/skilMgmtDetl')
        rr = {
            "result": r.text
        }

        return render(request, template_name, rr)

#공통 코드 조회
def retrieveCmmCd(request):
    param = json.loads(request.GET['param'])
    logger.info('param')
    logger.info(param)

    params = {
        'grp_id': param['grp_id'],
    }

    r = requests.get('http://skil_api:5003/retrieveCmmCd', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

#스킬 코드 관리 조회
def retrieveSkilCd(request) :
    logger.info("retrieveSkilCd : skil/views.py")
    param = json.loads(request.GET['param'])
    logger.info(param)

    datas = {
        'skilDiv': param['skilDiv']
    }

    logger.info(datas)
    r = requests.get('http://skil_api:5003/retrieveSkilCd', params=datas)

    # logger.info(r)
    # logger.info(r.text)
    # logger.info("----------------")
    # logger.info(r.json())
    # logger.info(json.loads(r.text))
    # # return JsonResponse(r.json())
    # return JsonResponse(r.json(), safe=False)

    paginator = Paginator(r.json(), 10)
    logger.info("----------------")
    logger.info(paginator)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")

    result = paginator.get_page(param['page'])

    logger.info(result)

    data = {
        'list': list(result.object_list),
        'total_records': paginator.count,
        'total_pages': paginator.num_pages,
        'page': result.number,
        'has_next': result.has_next(),
        'has_prev': result.has_previous()
    }

    # return JsonResponse(r.json())
    return JsonResponse(data)

#스킬 코드 조회
def getSkilCdMgmt(request):
    param = json.loads(request.GET['param'])
    logger.info('===============================')
    logger.info(param)
    logger.info('===============================')
    datas = {}

    r = requests.get('http://skil_api:5003/getskilCdMgmt', params=datas)

    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")
    logger.info(r.json())
    logger.info(json.loads(r.text))

    return JsonResponse(r.json(), safe=False)

#스킬 코드 삭제
def deleteSkilCd(request):
    param = json.loads(request.POST['param'])
    logger.info(param)
    datas = {
        'skilSno': param[0]['SKIL_SNO']
    }
    logger.info(datas)
    r = requests.post('http://skil_api:5003/deleteSkilCd', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json())

#스킬 코드 추가
def saveSkilCd(request):
    param = json.loads(request.POST['param'])
    logger.info(param)
    userId = str(request.user)
    for data in param:
        if '__created__' in data and data['__created__']:
            data['userId'] = userId
            r = requests.post('http://skil_api:5003/insertSkilCd', data=data)
        else:
            data['userId'] = userId
            r = requests.post('http://skil_api:5003/updateSkilCd', data=data)

    ret = {
        'result': 'OK'
    }
    return JsonResponse(ret)


def retrieveEmpSkilCd(request):
    param = json.loads(request.GET['param'])
    logger.info('param')
    logger.info(param)

    params = {

    }

    r = requests.get('http://skil_api:5003/retrieveEmpSkilCd', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

def deleteSkilDetl(request):
    param = json.loads(request.GET['param'])
    logger.info('param')
    logger.info(param)

    params = {
        'empNo': param['empNo'],
     }

    r = requests.get('http://skil_api:5003/deleteSkilDetl', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)


def saveSkilDetl(request):
    param = json.loads(request.GET['param'])
    logger.info('param')
    logger.info(param)

    params = {
        'empNo': param['empNo'],
        'skilNo': param['skilNo'],
    }

    r = requests.get('http://skil_api:5003/saveSkilDetl', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)