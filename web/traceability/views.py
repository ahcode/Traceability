from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import *

# Create your views here.
class Index(TemplateView):
    template_name = 'traceability/index.html'

class KeysList(ListView):
    model = Key
    template_name = 'traceability/keys_list.html'
    queryset = Key.objects.all()
    context_object_name = 'keys_list'
