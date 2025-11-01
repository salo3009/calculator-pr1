import math

def modulus(a, b):
    """Остаток от деления"""
    if b == 0:
        raise ValueError("Ошибка: Деление на ноль!")
    return a % b

def floor_divide(a, b):
    """Целочисленное деление"""
    if b == 0:
        raise ValueError("Ошибка: Деление на ноль!")
    return a // b

def floor(number):
    """Округление в меньшую сторону"""
    return math.floor(number)

def ceil(number):
    """Округление в большую сторону"""
    return math.ceil(number)