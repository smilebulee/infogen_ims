from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views import generic
from django.http import JsonResponse
import requests
import logging
import json

logger = logging.getLogger(__name__)

class Emp_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'emp/index.html'

        r = requests.get('http://emp_api:5000/hello')
        rr = {
            "result":r.text
        }
        
        return render(request, template_name, rr)


class Emp_api_testFox(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'emp/testFox.html'

        r = requests.get('http://emp_api:5000/hello')
        rr = {
            "result": r.text
        }

        return render(request, template_name, rr)

def testFox_ajax(request):

    param = json.loads(request.GET['param'])

    data = {
        'email' : param['email'],
        'password' : param['password'],
        'addr' : param['state'] + ' ' + param['city'] + ' ' + param['addr'] + ' ' + param['addrDetl'] + param['zip'],
        'sex' : param['chk']
    }

    r = requests.get('http://emp_api:5000/save',data)



    logger.info(data)
    return JsonResponse(data)