import math

def modulus(a, b):
    if b == 0:
        raise ValueError("Ошибка: Деление на ноль!")
    return a % b

def floor_divide(a, b):
    if b == 0:
        raise ValueError("Ошибка: Деление на ноль!")
    return a // b

def floor(number):
    return math.floor(number)

def ceil(number):
    return math.ceil(number)