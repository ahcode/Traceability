import os
API_URL = os.environ['TRACEABILITY_API_URL']
import requests
import json
import pyTraceability

def register_key(key_name,  public_key):
    json_data = {"name": key_name, "key": public_key}
    try:
        r = requests.post(API_URL + "/register", json_data)
    except:
        raise Exception("Connection error.")
    if (r.status_code != 200):
        raise Exception("Communication error. Status code: " + str(r.status_code))
    if (r.text != 'OK'):
        raise Exception("Communication error. " + r.text)

def send_transaction(transaction):
    try:
        headers={'Content-type': 'application/json', 'charset': 'utf-8'}
        r = requests.post(API_URL + "/newtransaction", headers = headers, data = transaction)
    except:
        raise Exception("Connection error.")
    if (r.text != 'OK'):
        raise Exception("Communication error. " + r.text)

def check_version():
    try:
        r = requests.get(API_URL + "/version")
    except:
        raise Exception("Connection error.")
    
    r = json.loads(r.text)
    if r['protocol_version'] != pyTraceability.protocol_version:
        raise Exception("Different protocol version between client and server.")

def check_key(keyhash):
    try:
        headers={'Content-type': 'application/json', 'charset': 'utf-8'}
        r = requests.post(API_URL + "/keycheck", headers = headers, data = json.dumps({'key' : keyhash}))
    except:
        raise Exception("Connection error.")

    r = json.loads(r.text)
    if r['status'] == 'ERROR':
        raise Exception("Error: " + r['error'])