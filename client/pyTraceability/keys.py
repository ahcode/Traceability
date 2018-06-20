# -*- coding: utf-8 -*-

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from pyTraceability import api_interface

class Key:
    def __init__(self, keyfile = None):
        #Generar una nueva clave
        if not keyfile:
            self.key = RSA.generate(1024)
        #Cargar clave desde fichero
        else:
            try:
                encoded_key = open(keyfile, "rb").read()
                self.key = RSA.import_key(encoded_key)
            except:
                raise Exception("Keyfile not found")

    #Almacenar la clave en un fichero
    def save_key(self, keyfile):
        file_out = open(keyfile, "wb")
        file_out.write(self.key.export_key())

    #Registrar la clave en el servidor
    def register_key(self, key_name):
        public_key = self.key.publickey().export_key()
        api_interface.register_key(key_name, public_key)
    
    #Obtener hash
    def get_hash(self):
        public_key = self.key.publickey().export_key()
        return SHA256.new(public_key).hexdigest()
    
    #Obtener la firma de una cadena de texto
    def get_sign(self, text):
        return "test"