import requests
import os
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import TransactionInput, Transaction, Origin
from django.conf import settings

def get_register_status():
    json_data = {"config_key": os.environ.get('REMOTE_CONFIG_KEY', '')}
    try:
        r = requests.post(os.environ.get('API_URL', '') + "/get_register_status", json_data, verify=settings.SSL_VERIFICATION)
        r_obj = json.loads(r.text)
        if r_obj['status'] == 'ERROR':
            return False
        else:
            return r_obj['remote_register']
    except:
        return False

def set_register_status(value):
    json_data = {"config_key": os.environ.get('REMOTE_CONFIG_KEY', ''), "remote_register": value}
    try:
        requests.post(os.environ.get('API_URL', '') + "/set_register_status", json_data, verify=settings.SSL_VERIFICATION)
    except:
        pass
    
def get_origins(product_id_obj):
    t_list = list(TransactionInput.objects.filter(t_hash = product_id_obj.last_transaction).values_list('input', flat=True))
    origin_dict = {}
    while t_list:
        t = t_list.pop()
        queryset = list(TransactionInput.objects.filter(t_hash = t).values_list('input', flat=True))
        if queryset:
            t_list.extend(queryset)
        else:
            t = Transaction.objects.get(hash = t)
            if t.type == 0:
                if not t.transaction_data['product'][0][0] in origin_dict:
                    origin_dict[t.transaction_data['product'][0][0]] = []
                try: o = Origin.objects.get(code = t.transaction_data['origin'])
                except ObjectDoesNotExist: o = t.transaction_data['origin']
                origin_dict[t.transaction_data['product'][0][0]].append(o)
    
    return origin_dict