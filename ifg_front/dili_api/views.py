from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views import generic
import requests

class Dili_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/index.html'

        return render(request, template_name)

class mariatest(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/mariatest.html'
        #화면 호출
        #r = requests.get('http://dili_api:5006/hello')
        rr = {
            "result": "123"
        }

        return render(request, template_name, rr)

def getMaria(request):
    param = json.loads(request.GET['param'])

    #api 호출
    r = requests.get('http://dili_api:5001/mariatestDB')
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    logger.info(json.loads(r.text))
    return JsonResponse(r.json(), safe=False)