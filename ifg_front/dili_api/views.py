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
import ast

logger = logging.getLogger(__name__)

class Dili_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/index.html'

        return render(request, template_name)

class scheduleMgmt(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/diliScheduleMgmt.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }

        return render(request, template_name)
        # return render(request, template_name, rr)

class mariatest(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/mariatest.html'
        # 화면 호출
        r = requests.get('http://dili_api:5006/hello')
        rr = {
            "result": r.text
        }

        return render(request, template_name, rr)



def getMaria(request):
    param = json.loads(request.GET['param'])

    logger.info("Start")
    logger.info(param)
    logger.info("End")

    # api 호출
    r = requests.get('http://dili_api:5006/mariatestDB')
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    logger.info(json.loads(r.text))
    return JsonResponse(r.json(), safe=False)

def getYryMgmt(request):
    param = json.loads(request.GET['param'])

    logger.info("Start")
    logger.info(param)
    logger.info("End")

    # api 호출
    r = requests.get('http://dili_api:5006/yryMgmt', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    logger.info(json.loads(r.text))
    return JsonResponse(r.json(), safe=False)

def getWrkTimeInfoByEml(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/wrkTimeInfoByEml', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

class wrkApvlReq(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/wrkApvlReqPopup.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }

        return render(request, template_name)
        # return render(request, template_name, rr)
    
class yryApvlReq(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/yryApvlReqPopup.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }
        return render(request, template_name)
        # return render(request, template_name, rr)

class noticeLst(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/noticeLst.html'


        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }
        return render(request, template_name)
        # return render(request, template_name, rr)


class noticeDtl(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/noticeDtl.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }
        return render(request, template_name)
        # return render(request, template_name, rr)

class empMgmt(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/empMgmt.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }
        return render(request, template_name)
        # return render(request, template_name, rr)


def getWrkApvlReq(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/wrkApvlReq', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)


def saveApvlReq(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    r = requests.post('http://dili_api:5006/saveApvlReq', data=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

class apvlReqHist(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/apvlReqHist.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }

        return render(request, template_name)
        # return render(request, template_name, rr)

def getApvlReqHist(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/apvlReqHist', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getApvlReqHistDetl(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/apvlReqHistDetl', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)