import ast
import io
import time
from contextlib import redirect_stdout
from pathlib import Path
from random import randint

from time_check import time_check


class TestTask3:
    @classmethod
    def setup_class(cls):
        # Проверяем декоратор cache_args из author.py
        # user_code предоставит платформа
        author_path = Path(__file__).parent.joinpath("author.py")
        with open(author_path) as user:
            cls.user_code = user.read()

        ast_user_code = ast.parse(cls.user_code)
        cls.cache_args_node = None
        for module_node in ast_user_code.body:
            if (
                isinstance(module_node, ast.FunctionDef)
                and module_node.name == "cache_args"
            ):
                cls.cache_args_node = module_node

        # Зададим случайные проверочные данные
        # Список передаваемых в функцию чисел
        cls.random_numerics = []

        # Они не должны повторяться
        def recursive_rand():
            rand = randint(0, 100)
            if rand in cls.random_numerics:
                return recursive_rand()
            else:
                return rand

        for _ in range(0, 4):
            cls.random_numerics.append(recursive_rand())
        # Случайный множитель
        cls.random_multiplier = randint(0, 100)

    def get_source_cache_args(self):
        assert (
            isinstance(self.cache_args_node, ast.FunctionDef)
        ), "Отсутствует функция cache_args."
        assign_count = 0
        function_count = 0
        for decorator_node in self.cache_args_node.body:
            if isinstance(decorator_node, ast.Assign):
                assign_count += 1
                assert (
                    assign_count == 1
                ), "Достаточно одного объявления переменной."
            elif isinstance(decorator_node, ast.FunctionDef):
                function_count += 1
                assert (
                    function_count == 1
                ), "Многовато вложенных функций. Можно проще."
                self.wrapper_name = decorator_node.name
            elif isinstance(decorator_node, ast.Return):
                pass
            else:
                assert (
                    False
                ), "Сложный декоратор. Можно упростить."

        source_cache_args = ast.get_source_segment(
            self.user_code, self.cache_args_node
        )
        return source_cache_args

    def cache_args(self, func):
        exec(self.get_source_cache_args())
        foo = vars()["cache_args"]
        return foo(func)

    def test_cache_args(self):
        # Декорируем некую функцию
        @time_check
        @self.cache_args
        def decorated(num):
            time.sleep(1)
            return num * self.random_multiplier

        def runing(t):
            for i in self.random_numerics:
                buffer = io.StringIO()
                with redirect_stdout(buffer):
                    result = decorated(i)
                assert (
                    result == i * self.random_multiplier
                ), "Некорректное решение."
                line = buffer.getvalue().strip()
                assert (
                    line == f"Время выполнения функции: {t} с."
                ), (
                    f"Некорректное время выполнения проверочной функции. "
                    "Функция возвращает:\n"
                    f"{line}\n"
                    f"Ожидалось {t} с."
                )

        # При первом запуске выполняется декорированная функция
        runing(1.0)
        # При повторном запуске ожидаем данных из кэша
        runing(0.0)
