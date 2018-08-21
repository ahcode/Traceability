import requests
import os
import json

def get_register_status():
    json_data = {"config_key": os.environ.get('REMOTE_CONFIG_KEY', '')}
    try:
        r = requests.post(os.environ.get('API_URL', '') + "/get_register_status", json_data)
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
        requests.post(os.environ.get('API_URL', '') + "/set_register_status", json_data)
    except:
        pass