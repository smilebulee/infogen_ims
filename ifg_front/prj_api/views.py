from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views import View
from django.views import generic
from django.http import JsonResponse
import requests
import logging

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