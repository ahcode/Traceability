from collections import OrderedDict
from time import time
import json
from pyTraceability.keys import Key
from pyTraceability.api_interface import send_transaction

class Connection():
    """Representa una conexión entre una etapa y el servidor.
    Sus métodos permiten comunicarse con el servidor de forma sencilla
    y realizar todo tipo de transacciones."""

    def __init__(self, keyfile: str):
        """Inicializa la conexión. Comprueba la conexión con el servidor así como la validez
        de la clave de la etapa."""
        self.key = Key(keyfile)

        self.__apicheck()

    def __apicheck(self):
        """Conecta con el servidor para comprobar su estado y valida la clave de conexión
        para asegurar que las transacciones posteriores sean aceptadas."""
        return
        #TODO

    def __newtransaction(self, transaction_type, mode, receiver, data):
        """Genera una transacción con el formato correcto, añade la firma y la envía al servidor."""
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

    def generate(self, origin: str, product: str, quantity: int, additional_data: dict = {}):
        """Transacción generadora.
        Añade materia prima a la cadena de producción. Es necesario especificar un identificador de origen.
        Se establece el modo de transacción por defecto como 0 (mezcla) ya que el servidor no distingue
        modos en transacciones generadoras."""

        data = {"product": (product, quantity), "origin": origin, **additional_data}
        self.__newtransaction(0, 0, None, data)
    
    def send(self, mode: int, receiver: str, product: str, quantity: int = None, additional_data: dict = {}):
        """Envía producto a otra etapa de la cadena.
        Permite 3 modos de selección del producto:
            0 - Mezcla
            1 - Cola
            2 - Pila
        Si no se especifica cantidad se enviará todo el producto que posee la etapa emisora."""
        
        if mode < 0 or mode > 2: raise Exception("mode must be between 0 and 2")

        data = {"product": (product, quantity), **additional_data}
        
        self.__newtransaction(2, mode, receiver, data)

    def send_by_id(self, receiver: str, product: str, product_id: str, additional_data: dict = {}):
        """Envía producto con id a otra etapa de la cadena.
        Utiliza el modo 3 (Arbitrario) para la selección del producto."""

        data = {"product": [product, product_id], **additional_data}

        self.__newtransaction(2, 3, receiver, data)
    
    def change_type(self, mode: str, product_in_list: list, product_out_list: list, receiver: str = None, additional_data: dict = {}):
        """Cambia de tipo uno o varios productos.
        Las listas de entrada y salida de productos deberán ser una lista de tuplas.
        Cada tupla incluirá el producto en su primer elemento y la cantidad en el segundo elemento.
        En la lista de entrada, la cantidad se puede establecer como 'None' para utilizar todo el producto disponible.
        Ej: [('in1', 5), ('in2', None), ...] - [('out1', 6), ('out2', 11), ...]
        Si no se indica receptor los productos de salida no cambiarán de etapa, seguirań perteneciendo al emisor."""

        if mode < 0 or mode > 2: raise Exception("mode must be between 0 and 2")

        data = {**additional_data}
        if product_in_list.length() == 1:
            data['product_in'] = product_in_list[0]
        else:
            data['product_in'] = product_in_list
        
        if product_out_list.length() == 1:
            data['product_out'] = product_out_list[0]
        else:
            data['product_out'] = product_out_list

        self.__newtransaction(2, mode, receiver, data)

    def change_type_by_id(self, product_in: str, id_in: str, product_out_list: list, receiver: str = None, additional_data: dict = {}):
        """Cambia de tipo de producto especificando un id para el producto de entrada.
        La cantidad de producto de entrada será siempre 1 ya que el identificador se asigna siempre a una unidad de producto.
        La lista de salida de productos deberá ser una lista de tuplas.
        Cada tupla incluirá el producto en su primer elemento y la cantidad en el segundo elemento.
        Ej: [('out1', 6), ('out2', 11), ...]
        Si no se indica receptor los productos de salida no cambiarán de etapa, seguirań perteneciendo al emisor."""

        data = {'product_in': (product_in, id_in), **additional_data}
        
        if product_out_list.length() == 1:
            data['product_out'] = product_out_list[0]
        else:
            data['product_out'] = product_out_list

        self.__newtransaction(2, 3, receiver, data)

    def end_product(self, mode: int, destination: str, product: str, quantity: int = None, additional_data: dict = {}):
        """Indica que un producto ha salido de la cadena de producción y su trazabilidad ha terminado.
        Es necesrio especificar un identificador de destino.
        Permite 3 modos de selección del producto:
            0 - Mezcla
            1 - Cola
            2 - Pila
        Si no se especifica cantidad se enviará todo el producto que posee la etapa emisora."""

        if mode < 0 or mode > 2: raise Exception("mode must be between 0 and 2")
        
        data = {"product": (product, quantity), "destination": destination, **additional_data}
        self.__newtransaction(1, mode, None, data)
    
    def end_by_id(self, destination: str, product: str, product_id: str, additional_data: dict = {}):
        """Indica que un producto con id ha salido de la cadena de producción y su trazabilidad ha terminado.
        Es necesrio especificar un identificador de destino.
        La cantidad de producto será siempre 1 ya que el identificador se asigna siempre a una unidad de producto."""

        data = {"product": (product, product_id), "destination": destination, **additional_data}
        self.__newtransaction(1, 3, None, data)


    def set_id(self, mode: int, product: str, new_id: str, receiver: str = None, additional_data: dict = {}):
        """Establece un identificador a una unidad de producto.
        Permite 3 modos de selección del producto:
            0 - Mezcla
            1 - Cola
            2 - Pila
        Si no se indica receptor el producto seguirá perteneciendo al emisor."""

        if mode < 0 or mode > 2: raise Exception("mode must be between 0 and 2")

        data = {"product": (product, 1), "new_id": new_id, **additional_data}
        self.__newtransaction(2, mode, receiver, data)