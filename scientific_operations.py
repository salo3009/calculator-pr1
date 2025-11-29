import math

def sin(degrees):
    return math.sin(math.radians(degrees))

def cos(degrees):
    return math.cos(math.radians(degrees))

def power(base, exponent):
    return base ** exponent

def square_root(number):
    if number < 0:
        raise ValueError("Ошибка: Корень из отрицательного числа!")
    return math.sqrt(number)