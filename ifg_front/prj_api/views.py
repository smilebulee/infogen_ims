from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views import View
from django.views import generic
from django.http import JsonResponse
import requests
import logging
import json

logger = logging.getLogger(__name__)

class Prj_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'prj/index.html'

        r = requests.get('http://prj_api:5002/hello')
        rr = {
            "result":r.text
        }
        
        return render(request, template_name, rr)

@login_required
def retrieve(request):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    params = {}  # get 일때 사용
    data = {
        'username':'bulee',
        'email':'bulee@infogen.co.kr'
    }

    # requests.get(url, params=params)
    res = requests.post('http://prj_api:5002/retrieve', headers=headers, json=data)        # data가 다층 구조일 땐 json.dumps(data) 사용

    if res.status_code == requests.codes.ok:
        retVal = res.json()
        retVal['status'] = 'ok'
    else:
        retVal = {
            'status':'fail'
        }
    logger.debug(retVal);
    return JsonResponse(retVal)


def prjReg(request):
    template_name = 'prj/prjReg.html'

    return render(request, template_name)

# 프로젝트 정보 조회
def retrievePrjInfo(request):
    param = json.loads(request.GET['param'])

    params = {
        'prj_cd': param['prj_cd'],
    }

    r = requests.get('http://prj_api:5002/retrievePrjInfo', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)


# 프로젝트 요구 스킬 조회
def retrieveReqSkil(request):
    param = json.loads(request.GET['param'])

    params = {
        'prj_cd': param['prj_cd'],
    }

    r = requests.get('http://prj_api:5002/retrieveReqSkil', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

# 프로젝트 저장
def prjSave(request):
    param = json.loads(request.POST['param'])

    datas = {
    }

    for row in param:
        datas.setdefault(row, param[row])

    r = requests.post('http://prj_api:5002/prjSave', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json())

# 프로젝트 삭제
def prjDelete(request):

    param = json.loads(request.POST['param'])

    datas = {
        'prj_name' : param['prj_name'],
        'prj_cnct_cd' : param['prj_cnct_cd'],
        'gnr_ctro'  : param['gnr_ctro'],
        'ctro': param['ctro'],
        'cnct_amt': param['cnct_amt'],
        'slin_bzdp': param['slin_bzdp'],
        'job_divs': param['job_divs'],
        'pgrs_stus' : param['pgrs_stus'],
        'req_skil_divs' : param['req_skil_divs1'],
        'req_skil_name' : param['req_skil_name1'],
        'rmks' : param['rmks'],
    }

    r = requests.post('http://prj_api:5002/prjDelete', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json())