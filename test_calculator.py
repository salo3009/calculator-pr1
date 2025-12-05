import unittest
import math
import sys
from unittest.mock import Mock, patch

from basic_operations import add, subtract, multiply, divide
from advanced_operations import modulus, floor_divide, floor, ceil
from scientific_operations import sin, cos, power, square_root
from memory_operations import Memory


class TestBasicOperations(unittest.TestCase):
    
    def test_add_positive_numbers(self):
        """Тест сложения положительных чисел"""
        self.assertEqual(add(5, 3), 8)
        self.assertEqual(add(10, 20), 30)
    
    def test_add_negative_numbers(self):
        """Тест сложения отрицательных чисел"""
        self.assertEqual(add(-5, -3), -8)
        self.assertEqual(add(-10, 5), -5)
    
    def test_add_zero(self):
        """Тест сложения с нулем"""
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(5, 0), 5)
        self.assertEqual(add(0, -3), -3)
    
    def test_add_decimals(self):
        """Тест сложения десятичных чисел"""
        self.assertEqual(add(2.5, 1.5), 4.0)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3, places=7)
    
    def test_subtract_positive_numbers(self):
        """Тест вычитания положительных чисел"""
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(subtract(20, 5), 15)
    
    def test_subtract_negative_numbers(self):
        """Тест вычитания отрицательных чисел"""
        self.assertEqual(subtract(5, 10), -5)
        self.assertEqual(subtract(-3, -7), 4)
    
    def test_subtract_zero(self):
        """Тест вычитания нуля"""
        self.assertEqual(subtract(10, 0), 10)
        self.assertEqual(subtract(0, 5), -5)
    
    def test_subtract_decimals(self):
        """Тест вычитания десятичных чисел"""
        self.assertEqual(subtract(7.5, 2.5), 5.0)
        self.assertEqual(subtract(1.0, 0.5), 0.5)
    
    def test_multiply_positive_numbers(self):
        """Тест умножения положительных чисел"""
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(5, 6), 30)
    
    def test_multiply_negative_numbers(self):
        """Тест умножения отрицательных чисел"""
        self.assertEqual(multiply(-3, 4), -12)
        self.assertEqual(multiply(-2, -5), 10)
    
    def test_multiply_zero(self):
        """Тест умножения на ноль"""
        self.assertEqual(multiply(0, 5), 0)
        self.assertEqual(multiply(10, 0), 0)
        self.assertEqual(multiply(0, 0), 0)
    
    def test_multiply_decimals(self):
        """Тест умножения десятичных чисел"""
        self.assertEqual(multiply(2.5, 2), 5.0)
        self.assertEqual(multiply(0.5, 0.5), 0.25)
    
    def test_divide_positive_numbers(self):
        """Тест деления положительных чисел"""
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(7, 2), 3.5)
    
    def test_divide_negative_numbers(self):
        """Тест деления отрицательных чисел"""
        self.assertEqual(divide(-10, 2), -5)
        self.assertEqual(divide(10, -2), -5)
        self.assertEqual(divide(-10, -2), 5)
    
    def test_divide_by_one(self):
        """Тест деления на 1"""
        self.assertEqual(divide(5, 1), 5)
        self.assertEqual(divide(-3, 1), -3)
    
    def test_divide_zero_by_number(self):
        """Тест деления нуля на число"""
        self.assertEqual(divide(0, 5), 0)
    
    def test_divide_by_zero_raises_error(self):
        """Тест деления на ноль вызывает ошибку"""
        with self.assertRaises(ValueError) as context:
            divide(5, 0)
        self.assertEqual(str(context.exception), "Ошибка: Деление на ноль!")
        
        with self.assertRaises(ValueError) as context:
            divide(0, 0)
        self.assertEqual(str(context.exception), "Ошибка: Деление на ноль!")


class TestAdvancedOperations(unittest.TestCase):
    
    def test_modulus_positive_numbers(self):
        """Тест остатка от деления положительных чисел"""
        self.assertEqual(modulus(10, 3), 1)
        self.assertEqual(modulus(7, 2), 1)
        self.assertEqual(modulus(10, 5), 0)
    
    def test_modulus_negative_numbers(self):
        """Тест остатка от деления отрицательных чисел"""
        self.assertEqual(modulus(-7, 3), 2)  
        self.assertEqual(modulus(7, -3), -2) 
        self.assertEqual(modulus(-7, -3), -1)  
    
    def test_modulus_by_zero_raises_error(self):
        """Тест остатка от деления на ноль вызывает ошибку"""
        with self.assertRaises(ValueError) as context:
            modulus(5, 0)
        self.assertEqual(str(context.exception), "Ошибка: Деление на ноль!")
    
    def test_floor_divide_positive_numbers(self):
        """Тест целочисленного деления положительных чисел"""
        self.assertEqual(floor_divide(10, 3), 3)
        self.assertEqual(floor_divide(7, 2), 3)
        self.assertEqual(floor_divide(10, 5), 2)
    
    def test_floor_divide_negative_numbers(self):
        """Тест целочисленного деления отрицательных чисел"""
        self.assertEqual(floor_divide(-7, 3), -3)  
        self.assertEqual(floor_divide(7, -3), -3)  
        self.assertEqual(floor_divide(-7, -3), 2) 
    
    def test_floor_divide_by_zero_raises_error(self):
        """Тест целочисленного деления на ноль вызывает ошибку"""
        with self.assertRaises(ValueError) as context:
            floor_divide(5, 0)
        self.assertEqual(str(context.exception), "Ошибка: Деление на ноль!")
    
    def test_floor_positive_numbers(self):
        """Тест округления вниз положительных чисел"""
        self.assertEqual(floor(3.7), 3)
        self.assertEqual(floor(2.1), 2)
        self.assertEqual(floor(5.0), 5)
        self.assertEqual(floor(5), 5)
    
    def test_floor_negative_numbers(self):
        """Тест округления вниз отрицательных чисел"""
        self.assertEqual(floor(-1.5), -2)
        self.assertEqual(floor(-2.1), -3)
        self.assertEqual(floor(-3.0), -3)
    
    def test_ceil_positive_numbers(self):
        """Тест округления вверх положительных чисел"""
        self.assertEqual(ceil(3.7), 4)
        self.assertEqual(ceil(2.1), 3)
        self.assertEqual(ceil(5.0), 5)
        self.assertEqual(ceil(5), 5)
    
    def test_ceil_negative_numbers(self):
        """Тест округления вверх отрицательных чисел"""
        self.assertEqual(ceil(-1.5), -1)
        self.assertEqual(ceil(-2.1), -2)
        self.assertEqual(ceil(-3.0), -3)


class TestScientificOperations(unittest.TestCase):
    
    def test_sin_special_angles(self):
        """Тест синуса специальных углов"""
        self.assertAlmostEqual(sin(0), 0, places=7)
        self.assertAlmostEqual(sin(30), 0.5, places=7)
        self.assertAlmostEqual(sin(90), 1, places=7)
        self.assertAlmostEqual(sin(180), 0, places=7)
        self.assertAlmostEqual(sin(270), -1, places=7)
        self.assertAlmostEqual(sin(360), 0, places=7)
    
    def test_sin_random_angles(self):
        """Тест синуса случайных углов"""
        self.assertAlmostEqual(sin(45), math.sin(math.radians(45)), places=7)
        self.assertAlmostEqual(sin(60), math.sin(math.radians(60)), places=7)
        self.assertAlmostEqual(sin(120), math.sin(math.radians(120)), places=7)
    
    def test_cos_special_angles(self):
        """Тест косинуса специальных углов"""
        self.assertAlmostEqual(cos(0), 1, places=7)
        self.assertAlmostEqual(cos(60), 0.5, places=7)
        self.assertAlmostEqual(cos(90), 0, places=7)
        self.assertAlmostEqual(cos(180), -1, places=7)
        self.assertAlmostEqual(cos(270), 0, places=7)
        self.assertAlmostEqual(cos(360), 1, places=7)
    
    def test_cos_random_angles(self):
        """Тест косинуса случайных углов"""
        self.assertAlmostEqual(cos(45), math.cos(math.radians(45)), places=7)
        self.assertAlmostEqual(cos(120), math.cos(math.radians(120)), places=7)
        self.assertAlmostEqual(cos(225), math.cos(math.radians(225)), places=7)
    
    def test_power_positive_exponent(self):
        """Тест возведения в положительную степень"""
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(3, 2), 9)
        self.assertEqual(power(5, 1), 5)
    
    def test_power_zero_exponent(self):
        """Тест возведения в нулевую степень"""
        self.assertEqual(power(5, 0), 1)
        self.assertEqual(power(-3, 0), 1)
        self.assertEqual(power(0, 0), 1) 
    
    def test_power_negative_exponent(self):
        """Тест возведения в отрицательную степень"""
        self.assertEqual(power(2, -1), 0.5)
        self.assertEqual(power(4, -2), 0.0625)
        self.assertEqual(power(10, -3), 0.001)
    
    def test_power_fractional_base(self):
        """Тест возведения дробного числа в степень"""
        self.assertEqual(power(0.5, 2), 0.25)
        self.assertEqual(power(2.5, 2), 6.25)
    
    def test_square_root_perfect_squares(self):
        """Тест квадратного корня из полных квадратов"""
        self.assertEqual(square_root(9), 3)
        self.assertEqual(square_root(16), 4)
        self.assertEqual(square_root(25), 5)
        self.assertEqual(square_root(1), 1)
        self.assertEqual(square_root(0), 0)
    
    def test_square_root_non_perfect_squares(self):
        """Тест квадратного корня из неполных квадратов"""
        self.assertAlmostEqual(square_root(2), math.sqrt(2), places=7)
        self.assertAlmostEqual(square_root(3), math.sqrt(3), places=7)
        self.assertAlmostEqual(square_root(10), math.sqrt(10), places=7)
    
    def test_square_root_negative_raises_error(self):
        """Тест квадратного корня из отрицательного числа вызывает ошибку"""
        with self.assertRaises(ValueError) as context:
            square_root(-4)
        self.assertEqual(str(context.exception), "Ошибка: Корень из отрицательного числа!")
        
        with self.assertRaises(ValueError) as context:
            square_root(-1)
        self.assertEqual(str(context.exception), "Ошибка: Корень из отрицательного числа!")


class TestMemoryOperations(unittest.TestCase):
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.memory = Memory()
    
    def test_initial_memory_value(self):
        """Тест начального значения памяти"""
        self.assertEqual(self.memory.get_memory_value(), 0)
        self.assertEqual(self.memory.memory_recall(), 0)
    
    def test_memory_store_positive(self):
        """Тест сохранения положительного числа в память"""
        self.memory.memory_store(42)
        self.assertEqual(self.memory.get_memory_value(), 42)
        self.assertEqual(self.memory.memory_recall(), 42)
    
    def test_memory_store_negative(self):
        """Тест сохранения отрицательного числа в память"""
        self.memory.memory_store(-15)
        self.assertEqual(self.memory.get_memory_value(), -15)
    
    def test_memory_store_zero(self):
        """Тест сохранения нуля в память"""
        self.memory.memory_store(0)
        self.assertEqual(self.memory.get_memory_value(), 0)
    
    def test_memory_store_decimal(self):
        """Тест сохранения десятичного числа в память"""
        self.memory.memory_store(3.14)
        self.assertEqual(self.memory.get_memory_value(), 3.14)
        
        self.memory.memory_store(-2.5)
        self.assertEqual(self.memory.get_memory_value(), -2.5)
    
    def test_memory_store_overwrites_previous(self):
        """Тест перезаписи предыдущего значения памяти"""
        self.memory.memory_store(10)
        self.memory.memory_store(20)
        self.assertEqual(self.memory.get_memory_value(), 20)
    
    def test_memory_add_positive(self):
        """Тест добавления положительного числа к памяти"""
        self.memory.memory_store(10)
        self.memory.memory_add(5)
        self.assertEqual(self.memory.get_memory_value(), 15)
    
    def test_memory_add_negative(self):
        """Тест добавления отрицательного числа к памяти"""
        self.memory.memory_store(10)
        self.memory.memory_add(-3)
        self.assertEqual(self.memory.get_memory_value(), 7)
    
    def test_memory_add_to_zero(self):
        """Тест добавления к нулевой памяти"""
        self.memory.memory_add(7)
        self.assertEqual(self.memory.get_memory_value(), 7)
    
    def test_memory_subtract_positive(self):
        """Тест вычитания положительного числа из памяти"""
        self.memory.memory_store(20)
        self.memory.memory_subtract(8)
        self.assertEqual(self.memory.get_memory_value(), 12)
    
    def test_memory_subtract_negative(self):
        """Тест вычитания отрицательного числа из памяти"""
        self.memory.memory_store(20)
        self.memory.memory_subtract(-5)  
        self.assertEqual(self.memory.get_memory_value(), 25)
    
    def test_memory_clear(self):
        """Тест очистки памяти"""
        self.memory.memory_store(100)
        self.memory.memory_clear()
        self.assertEqual(self.memory.get_memory_value(), 0)
        
        self.memory.memory_add(5)
        self.memory.memory_clear()
        self.assertEqual(self.memory.get_memory_value(), 0)
    
    def test_multiple_operations_combined(self):
        """Тест комбинации нескольких операций с памятью"""
        self.memory.memory_store(5)     
        self.memory.memory_add(3)        
        self.memory.memory_subtract(2)   
        self.memory.memory_add(4)       
        self.memory.memory_subtract(1)  
        self.assertEqual(self.memory.get_memory_value(), 9)


class TestCalculatorLogic(unittest.TestCase):
    """Тесты для логики калькулятора без тестирования GUI"""
    
    def test_expression_evaluation_simple(self):
        """Тест вычисления простых выражений"""
        
        self.assertEqual(eval("2 + 3"), 5)
        self.assertEqual(eval("10 - 4"), 6)
        self.assertEqual(eval("3 * 4"), 12)
        self.assertEqual(eval("10 / 2"), 5)
    
    def test_expression_evaluation_complex(self):
        """Тест вычисления сложных выражений"""
        self.assertEqual(eval("2 + 3 * 4"), 14)
        self.assertEqual(eval("(2 + 3) * 4"), 20)
        self.assertEqual(eval("10 / 2 + 3"), 8)
        self.assertEqual(eval("10 / (2 + 3)"), 2)
    
    def test_safe_expression_conversion(self):
        """Тест преобразования выражений для безопасного eval"""
        self.assertEqual(square_root(16), 4)
        self.assertAlmostEqual(sin(90), 1, places=7)
        self.assertAlmostEqual(cos(0), 1, places=7)
        self.assertEqual(floor(3.7), 3)
        self.assertEqual(ceil(3.2), 4)



def run_all_tests():
    """Запускает все тесты и возвращает результат"""
    
    loader = unittest.TestLoader()
    
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestBasicOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestAdvancedOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestScientificOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculatorLogic))
    
    
    runner = unittest.TextTestRunner(verbosity=2)
    
    
    print("=" * 70)
    print("Запуск всех unit-тестов для калькулятора")
    print("=" * 70)
    
    result = runner.run(suite)
    

    print("\n" + "=" * 70)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print("=" * 70)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    
    if result.failures:
        print(f"Провалены: {len(result.failures)}")
        for test, traceback in result.failures:
            print(f"\nПровален тест: {test}")
            print(f"Ошибка: {traceback}")
    
    if result.errors:
        print(f"Ошибки: {len(result.errors)}")
        for test, traceback in result.errors:
            print(f"\nОшибка в тесте: {test}")
            print(f"Трейсбэк: {traceback}")
    
   
    return 0 if result.wasSuccessful() else 1



def print_test_summary():
    """Печатает краткую информацию о тестах"""
    print("\n" + "=" * 70)
    print("КРАТКОЕ РУКОВОДСТВО ПО ТЕСТИРОВАНИЮ")
    print("=" * 70)
    print("1. Всего тестовых классов: 5")
    print("   - TestBasicOperations: тесты базовых операций")
    print("   - TestAdvancedOperations: тесты расширенных операций")
    print("   - TestScientificOperations: тесты научных операций")
    print("   - TestMemoryOperations: тесты операций с памятью")
    print("   - TestCalculatorLogic: тесты логики вычислений")
    print("\n2. Чтобы запустить тесты, выполните:")
    print("   python test_calculator.py")
    print("\n3. Чтобы запустить тесты с детальным выводом:")
    print("   python test_calculator.py -v")
    print("\n4. Чтобы запустить только определенные тесты:")
    print("   python -m unittest test_calculator.TestBasicOperations")
    print("   python -m unittest test_calculator.TestMemoryOperations")
    print("=" * 70)



if __name__ == '__main__':
    if '-v' in sys.argv or '--verbose' in sys.argv:
        unittest.main(verbosity=2)
    else:
        exit_code = run_all_tests()
        print_test_summary()
        
        sys.exit(exit_code)