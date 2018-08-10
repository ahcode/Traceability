#from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView, ListView
from django.contrib import messages
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

def ActivateKey(request, hash):
    try:
        k = Key.objects.get(hash = hash)
        k.current_status = 'active'
        k.save()
        messages.add_message(request, messages.SUCCESS, "La clave '" + k.name + "' se ha activado correctamente.")
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "No se ha encontrado la clave.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def DeactivateKey(request, hash):
    try:
        k = Key.objects.get(hash = hash)
        k.current_status = 'inactive'
        k.save()
        messages.add_message(request, messages.SUCCESS, "La clave '" + k.name + "' se ha desactivado correctamente.")
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "No se ha encontrado la clave.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def RemoveKey(request, hash):
    try:
        k = Key.objects.get(hash = hash)
        if k.current_status != 'new':
            messages.add_message(request, messages.ERROR, "No se pueden eliminar claves que ya han sido activadas.")
        else:
            k.delete()
            messages.add_message(request, messages.SUCCESS, "La clave '" + k.name + "' se ha eliminado correctamente.")
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "No se ha encontrado la clave.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))