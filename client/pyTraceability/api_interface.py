import os
API_URL = os.environ['TRACEABILITY_API_URL']
import requests

def register_key(key_name,  public_key):
    json_data = {"name": key_name, "key": public_key}
    try:
        r = requests.post(API_URL + "/register", json_data)
    except:
        raise Exception("Connection error.")
    if (r.status_code != 200):
        raise Exception("Communication error. Status code: " + r.status_code)
    if (r.text != 'OK'):
        raise Exception("Communication error. " + r.text)

def send_transaction(transaction):
    try:
        r = requests.post(API_URL + "/newtransaction", transaction)
    except:
        raise Exception("Connection error.")
    if (r.text != 'OK'):
        raise Exception("Communication error. " + r.text)