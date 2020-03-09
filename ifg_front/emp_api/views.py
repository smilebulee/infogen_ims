from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views import generic
import requests

class Emp_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'emp/index.html'

        r = requests.get('http://emp_api:5001/hello')
        rr = {
            "result":r.text
        }
        
        return render(request, template_name, rr)