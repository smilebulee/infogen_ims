from django.shortcuts import render, redirect
from django.core import serializers
from django.core.paginator import Paginator
# Create your views here.
from django.views import View
from django.views import generic
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Cd_grp, Cd
from datetime import datetime
from main.helpers import ajax_login_required
import requests
import json
import logging

logger = logging.getLogger(__name__)

class Cmm_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'cmm/index.html'

        return render(request, template_name)

@login_required
def codeMng(request):
    logger.info(request)
    template_name = 'cmm/codeMng.html'

    return render(request, template_name)

@ajax_login_required
def getCodes(request):
    param = json.loads(request.GET['param'])
    logger.info('===============================')
    logger.info(request.user)
    logger.info(param)
    logger.info('===============================')
    grps = param['grps']   # 코드그룹 배열
    data = {}

    for grp in grps:
        qs = Cd.objects.filter(grp_cd = grp).order_by('sort_ord').values('grp_cd', 'cmm_cd', 'cmm_nm', 'sort_ord', 'id')
        #logger.info(qs)
        #qs_json = serializers.serialize('json', qs)    values 가 없을 때 사용
        qs_json = list(qs)
        #logger.info(qs_json)
        data[grp] = qs_json

    logger.info(data)
    return JsonResponse(data)

@ajax_login_required
def getCodeGrps(request):
    param = json.loads(request.GET['param'])

    qs = Cd_grp.objects.all().order_by('sort_ord').values('grp_cd', 'grp_nm', 'sort_ord')

    paginator = Paginator(qs, 10)
    result = paginator.get_page(param['page'])

    logger.info('<<<<<<<<<<<<<<<< result >>>>>>>>>>>>>>>>>>')
    logger.info(list(result.object_list))

    data = {
        'list': list(result.object_list),
        'total_records': paginator.count,
        'total_pages': paginator.num_pages,
        'page': result.number,
        'has_next': result.has_next(),
        'has_prev': result.has_previous()
    }

    logger.info('<<<<<<<<<<<<<<<< data >>>>>>>>>>>>>>>>>>')
    logger.info(data)

    return JsonResponse(data)

@ajax_login_required
def saveGrp(request):
    param = json.loads(request.POST['param'])
    logger.info(param)

    for data in param:
        if '__created__' in data and data['__created__']:
            grp = Cd_grp(grp_cd=data['grp_cd'], grp_nm=data['grp_nm'], sort_ord=data['sort_ord'], create_dt=datetime.now(), update_dt=datetime.now())
            grp.save()
        else:
            grp = Cd_grp.objects.get(pk=data['grp_cd'])
            grp.grp_nm = data['grp_nm']
            grp.sort_ord = data['sort_ord']
            grp.save()

    ret = {
        'result':'OK'
    }
    return JsonResponse(ret)

@ajax_login_required
def deleteGrp(request):
    param = json.loads(request.POST['param'])
    logger.info(param)

    for data in param:
        grp = Cd_grp.objects.get(pk = data['grp_cd'])
        grp.delete()

    ret = {
        'result': 'OK'
    }
    return JsonResponse(ret)

@ajax_login_required
def saveCd(request):
    param = json.loads(request.POST['param'])
    logger.info(param)

    for data in param:
        if '__created__' in data and data['__created__']:
            cd = Cd(cmm_cd=data['cmm_cd'], cmm_nm=data['cmm_nm'], sort_ord=data['sort_ord'], create_dt=datetime.now(), update_dt=datetime.now(), grp_cd_id=data['grp_cd'])
            cd.save()
        else:
            cd = Cd.objects.get(pk = data['id'])
            cd.grp_nm = data['cmm_nm']
            cd.sort_ord = data['sort_ord']
            cd.save()

    ret = {
        'result': 'OK'
    }
    return JsonResponse(ret)

@ajax_login_required
def deleteCd(request):
    param = json.loads(request.POST['param'])
    logger.info(param)

    for data in param:
        cd = Cd.objects.get(pk = data['id'])
        cd.delete()

    ret = {
        'result': 'OK'
    }
    return JsonResponse(ret)