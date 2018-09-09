from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import *
from django.http import Http404
from traceability import utils
from traceability_web.settings import QR_HOSTNAME

#Clase de la que heredarán las vistas disponibles solo para administradores
class StaffRequired(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('login')
    def test_func(self):
        return self.request.user.is_staff

# Página de Inicio
class Index(TemplateView):
    template_name = 'traceability/index.html'

#Lista de claves activas
class ActiveKeysList(StaffRequired, ListView):
    model = Key
    template_name = 'traceability/keys/keyslist_active.html'
    queryset = Key.objects.filter(current_status = 'active')
    context_object_name = 'keys_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['remote_register'] = utils.get_register_status()
        return context

#Lista de claves pendientes de activación
class PendingKeysList(StaffRequired, ListView):
    model = Key
    template_name = 'traceability/keys/keyslist_pending.html'
    queryset = Key.objects.filter(current_status = 'new')
    context_object_name = 'keys_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['remote_register'] = utils.get_register_status()
        return context

#Lista de claves inactivas
class InactiveKeysList(StaffRequired, ListView):
    model = Key
    template_name = 'traceability/keys/keyslist_inactive.html'
    queryset = Key.objects.filter(current_status = 'inactive')
    context_object_name = 'keys_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['remote_register'] = utils.get_register_status()
        return context

#Vista detalle de claves
class KeyDetails(StaffRequired, DetailView):
    model = Key
    template_name = 'traceability/keys/key_details.html'
    slug_url_kwarg = 'hash'
    slug_field = 'hash'
    context_object_name = 'key'

#Activar una determinada clave
@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('login'))
def ActivateKey(request, hash):
    try:
        k = Key.objects.get(hash = hash)
        k.current_status = 'active'
        k.save()
        messages.add_message(request, messages.SUCCESS, "La clave '" + k.name + "' se ha activado correctamente.")
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "No se ha encontrado la clave.")
    return HttpResponseRedirect(request.GET.get('next', '/'))

#Desactivar una determinada clave
@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('login'))
def DeactivateKey(request, hash):
    try:
        k = Key.objects.get(hash = hash)
        k.current_status = 'inactive'
        k.save()
        messages.add_message(request, messages.SUCCESS, "La clave '" + k.name + "' se ha desactivado correctamente.")
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "No se ha encontrado la clave.")
    return HttpResponseRedirect(request.GET.get('next', '/'))

#Eliminar una determinada clave
@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('login'))
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
    return HttpResponseRedirect(request.GET.get('next', '/'))

#Vista formulario para añadir una nueva clave al sistema
class NewKey(StaffRequired, CreateView):
    model = Key
    fields = ['name', 'public_key', 'current_status', 'description']
    template_name = "traceability/keys/key_form.html"
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Se ha registrado la nueva clave.")
        return super().form_valid(form)

#Vista formulario para modificar una clave (solo nombre y descripción)
class ModifyKey(StaffRequired, UpdateView):
    model = Key
    fields = ['name', 'description']
    template_name = "traceability/keys/key_form.html"
    slug_url_kwarg = 'hash'
    slug_field = 'hash'
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Se ha actualizado la información.")
        return super().form_valid(form)

#Busca una clave registrada
@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('login'))
def KeySearch(request):
    searchbox = request.GET.get('sb')
    if searchbox:
        if Key.objects.filter(hash = searchbox).exists():
            url = reverse('key_details', kwargs={'hash': searchbox})
        else:
            k = Key.objects.filter(name = searchbox)
            if k.exists():
                url = reverse('key_details', kwargs={'hash': k[0].hash})
            else:
                messages.add_message(request, messages.ERROR, "No se ha encontrado la clave.")
                url = reverse('keys')
    else:
        url = reverse('keys')
    return HttpResponseRedirect(url)

#Lista de transacciones
class TransactionsList(ListView):
    model = Transaction
    template_name = 'traceability/transactions/transactions_list.html'
    context_object_name = 'transactions_list'
    paginate_by = 10

    def get_queryset(self):
        q = super().get_queryset()
        if 'mindate' in self.request.GET:
            q = q.filter(client_timestamp__gte=self.request.GET['mindate'])
        if 'maxdate' in self.request.GET:
            q = q.filter(client_timestamp__lte=self.request.GET['maxdate'])
        if 'key' in self.request.GET:
            q = q.filter(Q(transmitter__name=self.request.GET['key']) | Q(transmitter__hash=self.request.GET['key']))
        if 'origin' in self.request.GET:
            q = q.filter(transaction_data__origin=self.request.GET['origin'])
        if 'destination' in self.request.GET:
            q = q.filter(transaction_data__destination=self.request.GET['destination'])
        return q

#Búsqueda avanzada de transacciones
class AdvancedSearch(TemplateView):
    template_name = 'traceability/transactions/advanced_search.html'

#Vista detalle de transacciones
class TransactionDetail(DetailView):
    model = Transaction
    template_name = 'traceability/transactions/transaction_details.html'
    context_object_name = 't'
    slug_url_kwarg = 'hash'
    slug_field = 'hash'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context[self.context_object_name]:
            obj = context[self.context_object_name]
            context['sign'] = obj.verify_sign()
            if 'new_id' in obj.transaction_data: newid = obj.transaction_data['new_id']
            else: newid = None
            if 'product' in obj.transaction_data:
                context['product'] = self.make_product_list(obj.transaction_data['product'], newid)
                self.set_quantity(context['product'], obj.updated_quantity)
                self.set_pre_transactions(context['product'], obj.hash)
                self.set_post_transactions(context['product'], obj.hash)
            else:
                context['product_in'] = self.make_product_list(obj.transaction_data['product_in'])
                context['product_out'] = self.make_product_list(obj.transaction_data['product_out'], newid)
                self.set_quantity(context['product_in'], obj.updated_quantity)
                self.set_pre_transactions(context['product_in'], obj.hash)
                self.set_post_transactions(context['product_out'], obj.hash)
            if 'origin' in obj.transaction_data:
                try: context['origin'] = Origin.objects.get(code = obj.transaction_data['origin'])
                except ObjectDoesNotExist: pass
            if 'destination' in obj.transaction_data:
                try: context['destination'] = Destination.objects.get(code = obj.transaction_data['destination'])
                except ObjectDoesNotExist: pass

        return context

    #Genera la lista de productos
    def make_product_list(self, p_list, newid = None):
        l = []
        for p in p_list:
            l.append({})
            l[-1]['product'] = p[0]
            p_obj = None
            try:
                p_obj = Product.objects.get(code = p[0])
                l[-1]['name'] = p_obj.name
            except ObjectDoesNotExist:
                pass
            if newid:
                l[-1]['newid'] = newid
            elif isinstance(p[1], str):
                l[-1]['id'] = p[1]
            else:
                l[-1]['quantity'] = p[1]
                if p_obj:
                    l[-1]['unit'] = p_obj.measure_unit
                    l[-1]['multiplier'] = p_obj.multiplier
        return l

    # Establece la cantidad para aquellas transacciones que no la indiquen y cambia de unidad se fuese necesarios
    def set_quantity(self, p_list, updated_quantity):
        for p in p_list:
            if 'quantity' in p and p['quantity'] == None:
                p['quantity'] = updated_quantity[p['product']]
            if 'multiplier' in p:
                p['quantity'] /= p['multiplier']

    # Establece las transacciones anteriores de cada producto
    def set_pre_transactions(self, p_list, hash):
        for p in p_list:
            in_list = list(TransactionInput.objects.filter(t_hash = hash, product = p['product']).values_list('input', flat=True))
            p['pre'] = in_list

    #Establece las transacciones siguientes de cada producto
    def set_post_transactions(self, p_list, hash):
        for p in p_list:
            out_list = list(TransactionInput.objects.filter(input = hash, product = p['product']).values_list('t_hash', flat=True))
            p['post'] = out_list

#Cambia el estado del registro remoto enviando la petición correspondiente al servidor
@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('login'))
def ChangeRemoteRegisterStatus(request, value):
    if value == 'on' or value == 'off':
        utils.set_register_status(value)
    return HttpResponseRedirect(request.GET.get('next', '/'))

#Vista detalle de un producto identificado
class IdDetails(DetailView):
    model = ProductID
    template_name = 'traceability/products/product_details.html'
    context_object_name = 'p'
    slug_url_kwarg = 'id'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context[self.context_object_name]:
            context['origins'] = utils.get_origins(context[self.context_object_name])
            try:
                p = Product.objects.get(code = context[self.context_object_name].product)
                context['p_name'] = p.name
            except ObjectDoesNotExist:
                pass
            if context[self.context_object_name].destination:
                try: context['destination'] = Destination.objects.get(code = context[self.context_object_name].destination)
                except ObjectDoesNotExist: pass
        context['qr_hostname'] = QR_HOSTNAME
        return context

#Buscador de productos identificados
class IdSearch(View):
    def get(self, request):
        id = request.GET.get('id', None)
        if not id:
            return render(request, 'traceability/products/product_search.html')
        else:
            return redirect('id_details', id)

#Lista de tipos de productos
class ProductList(StaffRequired, ListView):
    model = Product
    template_name = 'traceability/config/product_list.html'
    context_object_name = 'product_list'
    paginate_by = 10

#Formulario para añadir un nuevo producto al sistema
class NewProduct(StaffRequired, CreateView):
    model = Product
    fields = ['code', 'name', 'measure_unit', 'multiplier', 'description']
    template_name = "traceability/config/product_form.html"
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Se ha registrado el nuevo producto.")
        return super().form_valid(form)

#Formulario para modificar un tipo de producto
class ModifyProduct(StaffRequired, UpdateView):
    model = Product
    fields = ['name', 'measure_unit', 'multiplier', 'description']
    template_name = "traceability/config/product_form.html"
    slug_url_kwarg = 'code'
    slug_field = 'code'
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Se ha modificado el producto.")
        return super().form_valid(form)

#Eliminar un tipo de producto
@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('login'))
def RemoveProduct(request, code):
    try:
        p = Product.objects.get(code = code)
        p.delete()
        messages.add_message(request, messages.SUCCESS, "El producto '" + code + "' se ha eliminado correctamente.")
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "No se ha encontrado el producto.")
    return redirect('config_products')

#Vista detalle de un tipo de producto
class ProductDetails(StaffRequired, DetailView):
    model = Product
    template_name = 'traceability/config/product_details.html'
    context_object_name = 'p'
    slug_url_kwarg = 'code'
    slug_field = 'code'

#Lista de orígenes registrados
class OriginList(StaffRequired, ListView):
    model = Origin
    template_name = 'traceability/config/origin_list.html'
    context_object_name = 'origin_list'
    paginate_by = 10

#Formulario para añadir un nuevo origen
class NewOrigin(StaffRequired, CreateView):
    model = Origin
    fields = ['code', 'name', 'description']
    template_name = "traceability/config/origin_form.html"
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Se ha registrado el nuevo orígen.")
        return super().form_valid(form)

#Vista detalle de un origen
class OriginDetails(StaffRequired, DetailView):
    model = Origin
    template_name = 'traceability/config/origin_details.html'
    context_object_name = 'o'
    slug_url_kwarg = 'code'
    slug_field = 'code'

#Formulario para modificar un origen
class ModifyOrigin(StaffRequired, UpdateView):
    model = Origin
    fields = ['name', 'description']
    template_name = "traceability/config/origin_form.html"
    slug_url_kwarg = 'code'
    slug_field = 'code'
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Se ha modificado el origen.")
        return super().form_valid(form)

#Eleminar un origen
@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('login'))
def RemoveOrigin(request, code):
    try:
        o = Origin.objects.get(code = code)
        o.delete()
        messages.add_message(request, messages.SUCCESS, "El origen '" + code + "' se ha eliminado correctamente.")
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "No se ha encontrado el origen.")
    return redirect('config_origins')

#Lista de destinos registrados
class DestinationList(StaffRequired, ListView):
    model = Destination
    template_name = 'traceability/config/destination_list.html'
    context_object_name = 'destination_list'
    paginate_by = 10

#Formulario para registrar un nuevo destino
class NewDestination(StaffRequired, CreateView):
    model = Destination
    fields = ['code', 'name', 'description']
    template_name = "traceability/config/destination_form.html"
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Se ha registrado el nuevo destino.")
        return super().form_valid(form)

#Vista detalle de destino
class DestinationDetails(StaffRequired, DetailView):
    model = Destination
    template_name = 'traceability/config/destination_details.html'
    context_object_name = 'd'
    slug_url_kwarg = 'code'
    slug_field = 'code'

#Formulario para modificar un destino
class ModifyDestination(StaffRequired, UpdateView):
    model = Destination
    fields = ['name', 'description']
    template_name = "traceability/config/destination_form.html"
    slug_url_kwarg = 'code'
    slug_field = 'code'
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Se ha modificado el destino.")
        return super().form_valid(form)

#Eliminar destino
@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('login'))
def RemoveDestination(request, code):
    try:
        o = Destination.objects.get(code = code)
        o.delete()
        messages.add_message(request, messages.SUCCESS, "El destino '" + code + "' se ha eliminado correctamente.")
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "No se ha encontrado el destino.")
    return redirect('config_destinations')