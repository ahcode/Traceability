from collections import OrderedDict
from time import time
import json
from pyTraceability.keys import Key
from pyTraceability.api_interface import send_transaction

#TRANSACTION MODES
# 0 - MERGE
# 1 - QUEUE
# 2 - STACK
# 3 - ARBITRARY (PRODUCT ID REQUIRED)

class Connection():
    def __init__(self, keyfile):
        self.__apicheck()

        if not isinstance(keyfile, str): raise Exception("keyfile must be a string")
        self.key = Key(keyfile)

    def __apicheck(self):
        return True
        #POR DEFINIR
        #Conectar a la api y esperar una determinada respuesta
        #Si no se recibe lanzar excepción

    def __newtransaction(self, transaction_type, mode, receiver, data):
        transmitter = self.key.get_hash()
        ordered_data = OrderedDict(sorted(data.items()))
        transaction = [("type", transaction_type), ("mode", mode), ("transmitter", transmitter)]
        if(receiver):
            transaction.append(("receiver", receiver))
        transaction.extend([("timestamp", int(time())), ("data", ordered_data)])
        transaction = OrderedDict(transaction)
        serialized_transaction = json.dumps(transaction, separators = (',',':'))
        sign = self.key.get_sign(serialized_transaction)
        transaction.update({"sign": sign})
        serialized_transaction = json.dumps(transaction, separators = (',',':'))
        send_transaction(serialized_transaction)

    def generate(self, product, quantity, origin, additional_data = {}):
        if not isinstance(product, str): raise Exception("product must be a string")
        if not isinstance(quantity, int): raise Exception("quantity must be an integer")
        if quantity <= 0: raise Exception("quantity must be greater than 0")
        if not isinstance(origin, str): raise Exception("origin must be a string")
        if not isinstance(additional_data, dict): raise Exception("additional_data must be a dictionary")

        data = {"product": product, "quantity": quantity, **additional_data}
        self.__newtransaction(0, 0, None, data)
    
    def send(self, mode, receiver, product, quantity = None, additional_data = {}):
        if not isinstance(mode, int): raise Exception("mode must be an integer")
        if mode < 0 or mode > 2: raise Exception("mode must be between 0 and 2")
        if not isinstance(receiver, str): raise Exception("product must be a string")
        if not isinstance(product, str): raise Exception("product must be a string")
        if quantity and not isinstance(quantity, int): raise Exception("quantity must be an integer or null")
        if quantity and quantity <= 0: raise Exception("quantity must be greater than 0")
        if not isinstance(additional_data, dict): raise Exception("additional_data must be a dictionary")
        
        data = {"product": product, **additional_data}
        if quantity: data['quantity'] = quantity
        
        self.__newtransaction(2, mode, receiver, data)

    def send_by_id(self, receiver, product, product_id, additional_data = {}):
        if not isinstance(receiver, str): raise Exception("product must be a string")
        if not isinstance(product, str): raise Exception("product must be a string")
        if not isinstance(product_id, 'str'): raise Exception("product_id must be a string")
        if not isinstance(additional_data, dict): raise Exception("additional_data must be a dictionary")

        data = {"product": product, "product_id": product_id, **additional_data}

        self.__newtransaction(2, 3, receiver, data)