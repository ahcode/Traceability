from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import *

# Create your views here.
class Index(TemplateView):
    template_name = 'traceability/index.html'

class ActiveKeysList(ListView):
    model = Key
    template_name = 'traceability/keys/keyslist_active.html'
    queryset = Key.objects.filter(current_status = 'active')
    context_object_name = 'keys_list'

class PendingKeysList(ListView):
    model = Key
    template_name = 'traceability/keys/keyslist_pending.html'
    queryset = Key.objects.filter(current_status = 'new')
    context_object_name = 'keys_list'

class InactiveKeysList(ListView):
    model = Key
    template_name = 'traceability/keys/keyslist_inactive.html'
    queryset = Key.objects.filter(current_status = 'inactive')
    context_object_name = 'keys_list'