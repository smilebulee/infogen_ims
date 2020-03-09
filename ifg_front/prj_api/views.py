from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views import generic
import requests

class Prj_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'prj/index.html'

        r = requests.get('http://prj_api:5002/hello')
        rr = {
            "result":r.text
        }
        
        return render(request, template_name, rr)