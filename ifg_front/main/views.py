from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views import View
from django.views import generic
from django.http import JsonResponse
from .forms import LoginForm
import requests
import logging
import json

logger = logging.getLogger(__name__)

class Main_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'main/index.html'

        return render(request, template_name)

@login_required
def sample(request, sample):
    logger.info('>>>>>>>>>>>>>>'+sample)
    template_name = 'sample/' + sample + '.html'

    return render(request, template_name)

@login_required
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

def login_form(request):
    template_name = 'main/login.html'
    form = LoginForm()
    return render(request, template_name, {'form': form})