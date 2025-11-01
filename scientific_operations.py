import math

def sin(degrees):
    """Синус угла в градусах"""
    return math.sin(math.radians(degrees))

def cos(degrees):
    """Косинус угла в градусах"""
    return math.cos(math.radians(degrees))

def power(base, exponent):
    """Возведение в степень"""
    return base ** exponent

def square_root(number):
    """Квадратный корень"""
    if number < 0:
        raise ValueError("Ошибка: Корень из отрицательного числа!")
    return math.sqrt(number)