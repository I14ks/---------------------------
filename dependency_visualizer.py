import subprocess
import argparse
import graphviz
from typing import Set, List
import unittest
from unittest.mock import patch  # Импортируем patch для тестов

class DependencyVisualizer:
    def __init__(self, package_name: str, max_depth: int):
        self.package_name = package_name
        self.max_depth = max_depth
        self.graph = graphviz.Digraph(format='png')

    def get_dependencies(self, package: str) -> List[str]:
        """Получает список зависимостей для указанного пакета."""
        try:
            result = subprocess.run(
                ["apt-cache", "depends", package],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            dependencies = []
            for line in result.stdout.splitlines():
                if line.strip().startswith("Depends:"):
                    dep = line.split("Depends:")[1].strip()
                    dependencies.append(dep)
            return dependencies
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Ошибка при выполнении apt-cache: {e.stderr.strip()}")

    def build_dependency_graph(self, package: str, current_depth: int, visited: Set[str]):
        """Рекурсивно строит граф зависимостей."""
        if current_depth > self.max_depth or package in visited:
            return

        visited.add(package)
        dependencies = self.get_dependencies(package)

        for dep in dependencies:
            self.graph.edge(package, dep)
            self.build_dependency_graph(dep, current_depth + 1, visited)

    def visualize(self, output_path: str):
        """Создает визуализацию графа зависимостей."""
        self.build_dependency_graph(self.package_name, 0, set())
        self.graph.render(output_path, view=True)

def parse_args():
    parser = argparse.ArgumentParser(description="Визуализатор зависимостей пакетов Ubuntu.")
    parser.add_argument("-p", "--package", required=True, help="Имя анализируемого пакета.")
    parser.add_argument("-d", "--depth", type=int, required=True, help="Максимальная глубина анализа зависимостей.")
    parser.add_argument("-o", "--output", required=True, help="Путь для сохранения визуализации графа.")
    return parser.parse_args()

def main():
    args = parse_args()
    visualizer = DependencyVisualizer(args.package, args.depth)
    try:
        visualizer.visualize(args.output)
    except RuntimeError as e:
        print(f"Ошибка: {e}")

# Тесты
class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        self.visualizer = DependencyVisualizer("test-package", 2)

    def test_get_dependencies(self):
        """Тестирует извлечение зависимостей."""
        with patch("subprocess.run") as mocked_run:
            mocked_run.return_value.stdout = """
Depends: dependency1
Depends: dependency2
"""
            dependencies = self.visualizer.get_dependencies("test-package")
            self.assertEqual(dependencies, ["dependency1", "dependency2"])

    def test_build_dependency_graph(self):
        """Тестирует построение графа."""
        with patch.object(self.visualizer, "get_dependencies", return_value=["dep1", "dep2"]):
            self.visualizer.build_dependency_graph("test-package", 0, set())
            edges = [line.strip() for line in self.visualizer.graph.body if "->" in line]
            self.assertIn('"test-package" -> dep1', edges)
            self.assertIn('"test-package" -> dep2', edges)

if __name__ == "__main__":
    main()
