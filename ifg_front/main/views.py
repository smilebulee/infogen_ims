from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views import generic
import requests


class Main_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'main/index.html'

        return render(request, template_name)

def sample(request):
    template_name = 'sample.html'

    return render(request, template_name)