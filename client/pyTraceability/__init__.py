from collections import OrderedDict
from time import time
import json
from pyTraceability.keys import Key
from pyTraceability.api_interface import send_transaction

class Connection():
    """Representa una conexión entre una etapa y el servidor.
    Sus métodos permiten comunicarse con el servidor de forma sencilla
    y realizar todo tipo de transacciones."""

    def __init__(self, keyfile):
        """Inicializa la conexión. Comprueba la conexión con el servidor así como la validez
        de la clave de la etapa."""
        if not isinstance(keyfile, str): raise Exception("keyfile must be a string")
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

    def generate(self, origin, product, quantity, additional_data = {}):
        """Transacción generadora.
        Añade materia prima a la cadena de producción. Es necesario especificar un identificador de origen.
        Se establece el modo de transacción por defecto como 0 (mezcla) ya que el servidor no distingue
        modos en transacciones generadoras."""
        if not isinstance(product, str): raise Exception("product must be a string")
        if not isinstance(quantity, int): raise Exception("quantity must be an integer")
        if quantity <= 0: raise Exception("quantity must be greater than 0")
        if not isinstance(origin, str): raise Exception("origin must be a string")
        if not isinstance(additional_data, dict): raise Exception("additional_data must be a dictionary")

        data = {"product": product, "quantity": quantity, **additional_data}
        self.__newtransaction(0, 0, None, data)
    
    def send(self, mode, receiver, product, quantity = None, additional_data = {}):
        """Envía producto a otra etapa de la cadena.
        Permite 3 modos de selección del producto:
            0 - Mezcla
            1 - Cola
            2 - Pila
        Si no se especifica cantidad se enviará todo el producto que posee la etapa emisora."""
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
        """Envía producto con id a otra etapa de la cadena.
        Utiliza el modo 3 (Arbitrario) para la selección del producto."""
        if not isinstance(receiver, str): raise Exception("product must be a string")
        if not isinstance(product, str): raise Exception("product must be a string")
        if not isinstance(product_id, 'str'): raise Exception("product_id must be a string")
        if not isinstance(additional_data, dict): raise Exception("additional_data must be a dictionary")

        data = {"product": product, "product_id": product_id, **additional_data}

        self.__newtransaction(2, 3, receiver, data)
    
    def change_type(self, mode, product_in_list, product_out_list, receiver = None, additional_data = {}):
        """Cambia de tipo uno o varios productos.
        La lista de productos de entrada se puede especificar de dos formas diferentes:
            1 - Especificando cantidad - Ej: [('p1', 5), ('p2', 10), ...]
            2 - Sin cantidades - Ej: ['p1', 'p2', 'p3'...]
        La lista de productos de salida debe indicar siempre las cantidades de cada producto.
        Ej: [('o1', 5), ('o2', 10), ...]
        Si no se indica receptor los productos de salida no cambiarán de etapa, seguirań
        perteneciendo al emisor."""
        return
        #TODO

    def change_type_by_id(self, product_in, id_in, product_out_list, receiver = None, additional_data = {}):
        """Cambia de tipo de producto especificando un id para el producto de entrada.
        La cantidad de producto será siempre 1 ya que el identificador se asigna siempre a una unidad de producto.
        La lista de productos de salida debe indicar siempre las cantidades de cada producto.
        Ej: [('o1', 5), ('o2', 10), ...]
        Si no se indica receptor los productos de salida no cambiarán de etapa, seguirań
        perteneciendo al emisor."""
        return
        #TODO

    def end_product(self, destination, product, quantity = None, additional_data = {}):
        """Indica que un producto ha salido de la cadena de producción y su trazabilidad ha terminado.
        Es necesrio especificar un identificador de destino.
        Si no se especifica cantidad se enviará todo el producto que posee la etapa emisora."""
        return
        #TODO
    
    def end_by_id(self, destination, product, product_id, additional_data = {}):
        """Indica que un producto con id ha salido de la cadena de producción y su trazabilidad ha terminado.
        Es necesrio especificar un identificador de destino.
        La cantidad de producto será siempre 1 ya que el identificador se asigna siempre a una unidad de producto."""
        return
        #TODO

    def set_id(self, mode, product, new_id, receiver = None, additional_data = {}):
        """Establece un identificador a una unidad de producto.
        Permite 3 modos de selección del producto:
            0 - Mezcla
            1 - Cola
            2 - Pila
        Si no se indica receptor el producto seguirá perteneciendo al emisor."""
        return
        #TODO