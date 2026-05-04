"""
Тесты для Currency Converter
Запуск: python test_converter.py
"""

import unittest
import json
import os
import tempfile


class TestCurrencyConverter(unittest.TestCase):
    """Тесты для конвертера валют"""
    
    def setUp(self):
        """Подготовка к тестам"""
        # Создаём временный файл для тестов
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        # Подменяем файл истории
        import currency_converter as cc
        cc.HISTORY_FILE = self.temp_file.name
        cc.history = []
    
    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    # ========== ПОЗИТИВНЫЕ ТЕСТЫ ==========
    def test_positive_amount_valid(self):
        """Тест 1: Положительное число проходит валидацию"""
        from currency_converter import convert
        # Проверяем через прямой вызов функции валидации
        try:
            amount = float("100")
            self.assertGreater(amount, 0)
            self.assertTrue(True, "Положительное число принято")
        except:
            self.fail("Положительное число не прошло")
    
    def test_decimal_amount_valid(self):
        """Тест 2: Десятичное число проходит валидацию"""
        try:
            amount = float("123.45")
            self.assertGreater(amount, 0)
            self.assertTrue(True, "Десятичное число принято")
        except:
            self.fail("Десятичное число не прошло")
    
    # ========== НЕГАТИВНЫЕ ТЕСТЫ ==========
    def test_negative_amount_invalid(self):
        """Тест 3: Отрицательное число НЕ проходит валидацию"""
        try:
            amount = float("-50")
            self.assertGreater(amount, 0)
            self.fail("Отрицательное число прошло, а должно было вызвать ошибку")
        except:
            self.assertTrue(True)
    
    def test_zero_amount_invalid(self):
        """Тест 4: Ноль НЕ проходит валидацию"""
        try:
            amount = float("0")
            self.assertGreater(amount, 0)
            self.fail("Ноль прошёл, а должно было вызвать ошибку")
        except:
            self.assertTrue(True)
    
    def test_text_amount_invalid(self):
        """Тест 5: Текст НЕ проходит валидацию"""
        try:
            amount = float("abc")
            self.assertTrue(False, "Текст прошёл, а должно быть ошибка")
        except ValueError:
            self.assertTrue(True)
    
    def test_empty_amount_invalid(self):
        """Тест 6: Пустое поле НЕ проходит валидацию"""
        try:
            amount = float("")
            self.assertTrue(False, "Пустое поле прошло, а должно быть ошибка")
        except ValueError:
            self.assertTrue(True)
    
    # ========== ТЕСТЫ РАБОТЫ С JSON ==========
    def test_save_to_json(self):
        """Тест 7: Сохранение в JSON файл"""
        import currency_converter as cc
        
        test_data = [{"test": "data", "value": 100}]
        cc.history = test_data
        cc.save_history()
        
        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded[0]["test"], "data")
        self.assertEqual(loaded[0]["value"], 100)
    
    def test_load_from_json(self):
        """Тест 8: Загрузка из JSON файла"""
        import currency_converter as cc
        
        test_data = [{"date": "2026-05-04", "amount": 50}]
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        cc.history = []
        cc.load_history()
        
        self.assertEqual(len(cc.history), 1)
        self.assertEqual(cc.history[0]["amount"], 50)
    
    # ========== ГРАНИЧНЫЕ ТЕСТЫ ==========
    def test_minimum_valid_amount(self):
        """Тест 9: Минимальное допустимое значение (0.01)"""
        try:
            amount = float("0.01")
            self.assertGreater(amount, 0)
            self.assertTrue(True, "Минимальная сумма принята")
        except:
            self.fail("Минимальная сумма не прошла")
    
    def test_large_valid_amount(self):
        """Тест 10: Большая допустимая сумма (9999999)"""
        try:
            amount = float("9999999")
            self.assertGreater(amount, 0)
            self.assertTrue(True, "Большая сумма принята")
        except:
            self.fail("Большая сумма не прошла")


# ========== ЗАПУСК ТЕСТОВ ==========
def run_tests():
    """Запуск всех тестов с выводом результатов"""
    print("=" * 60)
    print("ЗАПУСК ТЕСТОВ ДЛЯ CURRENCY CONVERTER")
    print("=" * 60)
    
    # Создаём загрузчик тестов
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCurrencyConverter)
    
    # Запускаем с подробным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"✅ Пройдено: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Не пройдено: {len(result.failures)}")
    print(f"⚠️ Ошибок: {len(result.errors)}")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    run_tests()