from enum import Enum

class OrderStatus(Enum):
    '''Para limitar las opciones que el atributo status pueda almacenar'''
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

#la defino  aca porque primero debe estar definido OrderStatus
choices = [ (tag, tag.value) for tag in OrderStatus ]