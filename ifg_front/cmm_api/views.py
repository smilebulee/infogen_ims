from django.shortcuts import render, redirect
from django.core import serializers
# Create your views here.
from django.views import View
from django.views import generic
from django.http import JsonResponse, HttpResponseRedirect
from .models import Cd_grp, Cd
import requests
import json
import logging

logger = logging.getLogger(__name__)

class Cmm_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'cmm/index.html'

        return render(request, template_name)

def getCodes(request):
    param = json.loads(request.GET['param'])
    logger.info('===============================')
    logger.info(param)
    logger.info('===============================')
    grps = param['grps']   # 코드그룹 배열
    data = {}

    for grp in grps:
        qs = Cd.objects.filter(grp_cd = grp).order_by('sort_ord').values('grp_cd', 'cmm_cd', 'cmm_nm')
        #logger.info(qs)
        #qs_json = serializers.serialize('json', qs)    values 가 없을 때 사용
        qs_json = list(qs)
        #logger.info(qs_json)
        data[grp] = qs_json

    logger.info(data)
    return JsonResponse(data)