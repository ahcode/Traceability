# -*- coding: utf-8 -*-

from Crypto.PublicKey import RSA
from pyTraceability import api_interface

class Key:
    def __init__(self, keyfile = None):
        #Generar una nueva clave
        if not keyfile:
            self.key = RSA.generate(1024)
        #Cargar clave desde fichero
        else:
            encoded_key = open(keyfile, "rb").read()
            self.key = RSA.import_key(encoded_key)

    #Almacenar la clave en un fichero
    def save_key(self, keyfile):
        file_out = open(keyfile, "wb")
        file_out.write(self.key.export_key())

    #Registrar la clave en el servidor
    def register_key(self, key_name):
        public_key = self.key.publickey().export_key()
        api_interface.register_key(key_name, public_key)
