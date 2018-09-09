import os
API_URL = os.environ['TRACEABILITY_API_URL']
import requests
import json
import pyTraceability

verify = os.environ.get('DISABLE_SSL_VALIDATION', '') != 'TRUE'

#Registrar nueva clave
def register_key(key_name,  public_key):
    json_data = {"name": key_name, "key": public_key}
    try:
        r = requests.post(API_URL + "/register", json_data, verify=verify)
    except:
        raise Exception("Connection error.")
    
    r_obj = json.loads(r.text)
    if r_obj['status'] == 'ERROR':
        raise Exception("Communication error. " + r_obj['error'])

#Enviar una transacción
def send_transaction(transaction):
    try:
        headers={'Content-type': 'application/json', 'charset': 'utf-8'}
        r = requests.post(API_URL + "/newtransaction", headers = headers, data = transaction, verify=verify)
    except:
        raise Exception("Connection error.")
    
    r_obj = json.loads(r.text)
    if r_obj['status'] == 'ERROR':
        raise Exception("Communication error. " + r_obj['error'])

#Comprobar versión de protocolo
def check_version():
    try:
        r = requests.get(API_URL + "/version", verify=verify)
    except:
        raise Exception("Connection error.")
    
    r_obj = json.loads(r.text)
    if r_obj['status'] == 'ERROR':
        raise Exception("Error checking server version.")
    if r_obj['protocol_version'] != pyTraceability.protocol_version:
        raise Exception("Different protocol version between client and server.")

#Comprobar clave
def check_key(keyhash):
    try:
        headers={'Content-type': 'application/json', 'charset': 'utf-8'}
        r = requests.post(API_URL + "/keycheck", headers = headers, data = json.dumps({'key' : keyhash}), verify=verify)
    except:
        raise Exception("Connection error.")

    r_obj = json.loads(r.text)
    if r_obj['status'] == 'ERROR':
        raise Exception("Error: " + r_obj['error'])