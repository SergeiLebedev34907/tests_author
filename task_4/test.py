from random import randint

from author import make_divider_of


class TestTask4:
    @classmethod
    def setup_class(cls):
        # Количество делимых
        cls.dividend_count = 50
        # Минимальное и масимальное возможное значение делимого
        cls.min_dividend = -9999
        cls.max_dividend = 9999
        # Количество делителей для каждго делимого
        cls.divisor_count = 50
        # Минимальное и масимальное возможное значение делителя
        cls.min_divisor = -50
        cls.max_divisor = 50

        # Случайный список делимых
        cls.dividends = [
            randint(cls.min_dividend, cls.max_dividend) for _ in range(
                cls.dividend_count
            )
        ]

    def test_make_divider_of(self):
        for _ in range(self.divisor_count):
            # Случайный делитель
            divisor = randint(self.min_divisor, self.max_divisor)
            # Избегаем деления на 0
            if divisor == 0:
                continue
            # Создаем функцию и проверяем ее
            div_function = make_divider_of(divisor)
            for dividend in self.dividends:
                result = dividend/divisor
                function_result = div_function(dividend)
                assert (
                    function_result == result
                ), (
                    f"{function_result} - неверный результат функции для "
                    f"делимого {dividend} и делителя {dividend}."
                )
