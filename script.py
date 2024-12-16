import sys
import yaml
import argparse

class ConfigLanguageTranslator:
    def __init__(self):
        self.constants = {}

    def translate(self, yaml_data):
        """Трансформирует YAML-данные в учебный конфигурационный язык."""
        if not isinstance(yaml_data, dict):
            raise ValueError("Корневой элемент YAML должен быть объектом (dict).")

        result = []
        for key, value in yaml_data.items():
            if not self._is_valid_name(key):
                raise ValueError(f"Недопустимое имя: {key}")

            if isinstance(value, (int, float)):
                result.append(self._define_constant(key, value))
            elif isinstance(value, list):
                result.append(self._define_constant(key, self._translate_array(value)))
            else:
                raise ValueError(f"Неизвестный тип значения для ключа '{key}': {type(value)}")

        return "\n".join(result)

    def _define_constant(self, name, value):
        """Создает строку объявления константы."""
        return f"(def {name} {value});"

    def _translate_array(self, array):
        """Преобразует массив в строку формата конфигурационного языка."""
        if not all(isinstance(el, (int, float)) for el in array):
            raise ValueError("Массивы могут содержать только числа.")
        return "{ " + ", ".join(map(str, array)) + " }"

    def _is_valid_name(self, name):
        """Проверяет валидность имени."""
        return name.isidentifier()


def main():
    parser = argparse.ArgumentParser(description="YAML to Config Language Translator")
    parser.add_argument("output", help="Путь к выходному файлу")
    args = parser.parse_args()

    try:
        # Чтение YAML из стандартного ввода
        input_data = sys.stdin.read()
        yaml_data = yaml.safe_load(input_data)

        # Трансляция
        translator = ConfigLanguageTranslator()
        output_data = translator.translate(yaml_data)

        # Запись в файл
        with open(args.output, "w") as f:
            f.write(output_data)

        print(f"Файл успешно создан: {args.output}")
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
