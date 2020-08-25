from django.shortcuts import render, redirect
# Create your views here.

from django.views import View
from django.views import generic
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Tb_tpt
from main.helpers import ajax_login_required

import requests
import logging
import json

logger = logging.getLogger(__name__)
class Cnc_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'cnc/index.html'

        return render(request, template_name)

@login_required
def test2(request):
    logger.info("============test===================")
    template_name = 'cnc/test.html'

    return render(request, template_name)

def getTestview(request):
    param = json.loads(request.GET['param'])

    #쿼리 조회 CNC_API_TB_TPT Table 조회
    qs = Tb_tpt.objects.all().values('test_id','text_data','reg_user')
    logger.info(qs)
    logger.info(list(qs))
    data = {
        'list': list(qs)
    }
    return JsonResponse(data)