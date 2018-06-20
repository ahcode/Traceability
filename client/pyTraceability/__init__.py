from collections import OrderedDict
from time import time
import json
from pyTraceability.keys import Key
from pyTraceability.api_interface import send_transaction

class Connection():
    def __init__(self, keyfile, mode):
        self.__apicheck()

        if not isinstance(keyfile, str): raise Exception("keyfile must be a string")
        self.key = Key(keyfile)

        if mode == 'merge': self.mode = 0
        elif mode == 'queue': self.mode = 1
        elif mode == 'stack': self.mode = 2
        elif mode == 'arbitrary': self.mode = 3
        else: raise Exception("mode must be 'merge', 'serial' or 'arbitrary'")

    def __apicheck(self):
        return True
        #POR DEFINIR
        #Conectar a la api y esperar una determinada respuesta
        #Si no se recibe lanzar excepción

    def __newtransaction(self, transaction_type, transmitter, receiver, data):
        ordered_data = OrderedDict(sorted(data.items()))
        transaction = [("type", transaction_type), ("mode", self.mode), ("transmitter", transmitter), ("timestamp", int(time())), ("data", ordered_data)]
        transaction = OrderedDict(transaction)
        serialized_transaction = json.dumps(transaction, separators = (',',':'))
        sign = self.key.get_sign(serialized_transaction)
        transaction.update({"sign": sign})
        serialized_transaction = json.dumps(transaction, separators = (',',':'))
        send_transaction(serialized_transaction)


    def generate(self, product, quantity, origin, *args, **kwargs):
        if not isinstance(product, str): raise Exception("product must be a string")
        if not isinstance(quantity, int): raise Exception("quantity must be an integer")
        if quantity <= 0: raise Exception("quantity must be greater than 0")
        if not isinstance(origin, str): raise Exception("origin must be a string")

        data = {"product": product, "quantity": quantity, **kwargs}
        self.__newtransaction(0, self.key.get_hash(), None, data)