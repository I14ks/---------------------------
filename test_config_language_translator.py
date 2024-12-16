import unittest
from io import StringIO
import sys
import yaml
from script import ConfigLanguageTranslator  # Импортируйте класс из вашего скрипта

class TestConfigLanguageTranslator(unittest.TestCase):

    def setUp(self):
        """Подготовка тестов (в случае необходимости)."""
        self.translator = ConfigLanguageTranslator()

    def test_translate_single_constant(self):
        """Тестируем перевод одиночной константы."""
        yaml_data = {'constant1': 42}
        expected_output = "(def constant1 42);"
        output = self.translator.translate(yaml_data)
        self.assertEqual(output, expected_output)

    def test_translate_float_constant(self):
        """Тестируем перевод константы с плавающей точкой."""
        yaml_data = {'constant2': 3.14}
        expected_output = "(def constant2 3.14);"
        output = self.translator.translate(yaml_data)
        self.assertEqual(output, expected_output)

    def test_translate_list(self):
        """Тестируем перевод списка чисел."""
        yaml_data = {'list1': [1, 2, 3]}
        expected_output = "(def list1 { 1, 2, 3 });"
        output = self.translator.translate(yaml_data)
        self.assertEqual(output, expected_output)

    def test_invalid_name(self):
        """Тестируем ошибку для недопустимого имени ключа."""
        yaml_data = {'123constant': 42}
        with self.assertRaises(ValueError) as context:
            self.translator.translate(yaml_data)
        self.assertEqual(str(context.exception), "Недопустимое имя: 123constant")

    def test_invalid_array_elements(self):
        """Тестируем ошибку для массива, содержащего нечисловые значения."""
        yaml_data = {'list1': [1, 2, 'three']}
        with self.assertRaises(ValueError) as context:
            self.translator.translate(yaml_data)
        self.assertEqual(str(context.exception), "Массивы могут содержать только числа.")

    def test_non_dict_yaml(self):
        """Тестируем ошибку, когда корневой элемент YAML не является словарем."""
        yaml_data = ['item1', 'item2']
        with self.assertRaises(ValueError) as context:
            self.translator.translate(yaml_data)
        self.assertEqual(str(context.exception), "Корневой элемент YAML должен быть объектом (dict).")

    def test_empty_yaml(self):
        """Тестируем пустой YAML."""
        yaml_data = {}
        output = self.translator.translate(yaml_data)
        self.assertEqual(output, "")

    def test_translate_multiple_constants(self):
        """Тестируем перевод нескольких констант и списков."""
        yaml_data = {
            'constant1': 42,
            'constant2': 3.14,
            'list1': [1, 2, 3]
        }
        expected_output = "(def constant1 42);\n(def constant2 3.14);\n(def list1 { 1, 2, 3 });"
        output = self.translator.translate(yaml_data)
        self.assertEqual(output, expected_output)

    def test_translate_with_invalid_type(self):
        """Тестируем ошибку при передаче значения неподдерживаемого типа."""
        yaml_data = {'invalid': {'nested': 'structure'}}
        with self.assertRaises(ValueError) as context:
            self.translator.translate(yaml_data)
        self.assertEqual(str(context.exception), "Неизвестный тип значения для ключа 'invalid': <class 'dict'>")

if __name__ == "__main__":
    unittest.main()
