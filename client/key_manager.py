# -*- coding: utf-8 -*-

from pyTraceability import Key
import os
import sys

keys_folder = os.path.dirname(os.path.abspath(__file__)) + "/keys/"

key = None
key_name = None
fich = None

#Primer menú
def menu():
    opcion = 0
    while(opcion < 1 or opcion > 3):
        print("1. Generar nueva clave.\n2. Cargar clave desde fichero.\n3. Salir.")
        opcion = int(input("Introduce una opción: "))
    if(opcion == 1):
        new_key()
    elif(opcion == 2):
        load_key()
    else:
        sys.exit()
    menu2()

#Segundo menú
def menu2():
    opcion = 0
    while(opcion < 1 or opcion > 3):
        print("1. Registar clave en el servidor.\n2. Eliminar clave.\n3. Salir.")
        opcion = int(input("Introduce una opción: "))
    if(opcion == 1):
        global key
        key.register_key(key_name)
    elif(opcion == 2):
        os.remove(fich)
    else:
        sys.exit()

#Cargar clave de fichero
def load_key():
    global key_name
    global fich
    global key
    key_name = input("Introduce el nombre de la clave: ")
    fich = keys_folder + key_name + ".pem"
    if (not os.path.isfile(fich)):
        print("La clave especificada no existe.")
    else:
        global key
        key = Key(fich)

#Generar nueva clave
def new_key():
    global key
    global fich
    global key_name
    key = Key()
    key_name = input("Introduce el nombre de la clave: ")
    fich = keys_folder + key_name + ".pem"
    if (os.path.isfile(fich)):
        print("El nombre elegido ya existe.")
    key.save_key(fich)

#Bucle Principal
while True:
    menu()