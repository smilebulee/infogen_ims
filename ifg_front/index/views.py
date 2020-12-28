from django.shortcuts import render

# Create your views here.
from django.views import View
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
import requests

class Index(generic.TemplateView):
    def get(self, request, *args, **kwargs):

        return HttpResponseRedirect(reverse('main:mainImsPage'))