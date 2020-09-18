from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views import generic
from django.http import JsonResponse

#from .models import Tb_page

from django.views.decorators.csrf import csrf_exempt

import requests
import logging
import json

logger = logging.getLogger(__name__)

class Skil_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'skil/index.html'
        logger.info("dadadadaata")
        r = requests.get('http://skil_api:5003/hello')
        rr = {
            "result": r.text
        }

        return render(request, template_name,rr)

def devEnrl(request):
    template_name = 'skil/devEnrl.html'

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

def devSave(request):

    param = json.loads(request.POST['param'])

    datas = {
        'name' : param['name'],
        'rank' : param['rank'],
        'grd'  : param['grd'],
        'tlno1': param['tlno1'],
        'tlno2': param['tlno2'],
        'tlno3': param['tlno3'],
        'divs' : param['divs'],
        'blco' : param['blco'],
        'bday' : param['bday'],
        'rmks' : param['rmks'],

    }
    logger.info('request.post : ' + request.POST['param'])
    logger.info(datas)
    r = requests.post('http://skil_api:5003/devSave', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

def prjSave(request):

    param = json.loads(request.POST['param'])

    logger.info(param)

    datas = {
        'prj_nm' : param['prj_nm'],
        'cnct_cd' : param['cnct_cd'],
        'gnr_ctro'  : param['gnr_ctro'],
        'ctro': param['ctro'],
        'cnct_amt': param['cnct_amt'],
        'slin_bzdp': param['slin_bzdp'],
        'job_divs': param['job_divs'],
        'pgrs_stus' : param['pgrs_stus'],
        'req_skil_divs' : param['req_skil_divs'],
        'req_skil_name' : param['req_skil_name'],
        'rmks' : param['rmks'],

    }
    logger.info('request.post : ' + request.POST['param'])
    logger.info(datas)
    r = requests.post('http://skil_api:5003/prjSave', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

def prjInpuMgmt(request):
    template_name = 'skil/prjInpuMgmt.html'

    return render(request, template_name)

def skilMgmt(request):
    template_name = 'skil/skilMgmt.html'

    return render(request, template_name)

def prjInpuSearch(request):

    param = json.loads(request.GET['param'])
    logger.info("prjInpuSearch : skil/views.py")
    datas = {
        'prjCd': param['prjCd']
    }

    logger.info(datas)
    r = requests.get('http://skil_api:5003/prjInpuSearch', params=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")
    logger.info(r.json())
    logger.info(json.loads(r.text))
    return JsonResponse(r.json(), safe=False)

def prjInpuDelete(request):

    param = json.loads(request.POST['param'])
    logger.info(param)
    logger.info("prjInpuDelete : skil/views.py")
    datas = {
        'prjCd': param['PRJ_CD'],
        'empNo': param['EMP_NO'],
    }

    logger.info('request.post : ' + request.POST['param'])

    r = requests.post('http://skil_api:5003/prjInpuDelete', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")
    logger.info(r.json())
    logger.info(json.loads(r.text))
    return JsonResponse(r.json(), safe=False)

def skilMgmtSearch(request):

    param = json.loads(request.GET['param'])
    logger.info("skilMgmtSearch : skil/views.py")
    datas = {
        'dept': param['dept'],
        'name': param['name'],
        'division': param['division'],
        'skilKind': param['skilKind'],
        'skil': param['skil']
    }

    logger.info(datas)
    r = requests.get('http://skil_api:5003/skilMgmtSearch', params=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")
    logger.info(r.json())
    logger.info(json.loads(r.text))
    # return JsonResponse(r.json())
    return JsonResponse(r.json(), safe=False)

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