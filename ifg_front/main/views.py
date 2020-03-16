from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views import generic
from django.http import JsonResponse
import requests
import logging
import json

logger = logging.getLogger(__name__)

class Main_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'main/index.html'

        return render(request, template_name)

def sample(request, sample):
    logger.info('>>>>>>>>>>>>>>'+sample)
    template_name = 'sample/' + sample + '.html'

    return render(request, template_name)

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