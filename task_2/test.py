import ast
import io
from contextlib import redirect_stdout
from random import randint

from author import Contact as StudentContact
from precode import Contact as BaseContact


class TestOutput:
    # user_code — переменная, в которой в виде строки хранится весь код
    # студента.
    # output — stdout работы файла с кодом студента (все его print()) в
    # виде одной строки.
    # Потребуется переопределение переменных user_code и output для реальной
    # работы с платформой.
    @classmethod
    def setup_class(cls):
        cls.user_code = (
            "class Contact:\n"
            "    def __init__(self, name, phone, birthday, address):\n"
            "        self.name = name\n"
            "        self.phone = phone\n"
            "        self.birthday = birthday\n"
            "        self.address = address\n"
            "        print(f'Создаём новый контакт {name}')\n"
            "\n"
            "    # здесь напишите метод show_contact()\n"
            "    # он будет очень похож на функцию print_contact()\n"
            "    def show_contact(self):\n"
            "        print(f'{self.name} — адрес: {self.address}, телефон: "
            "{self.phone}, день рождения: {self.birthday}')\n"
            "\n"
            "\n"
            "mike = Contact('Михаил Булгаков', '2-03-27', '15.05.1891', "
            "'Россия, Москва, Большая Пироговская, дом 35б, кв. 6')\n"
            "vlad = Contact('Владимир Маяковский', '73-88', '19.07.1893', "
            "'Россия, Москва, Лубянский проезд, д. 3, кв. 12')\n"
            "\n"
            "mike.show_contact()\n"
            "vlad.show_contact()\n"
        )
        cls.output = (
            "Создаём новый контакт Михаил Булгаков\n"
            "Создаём новый контакт Владимир Маяковский\n"
            "Михаил Булгаков — адрес: Россия, Москва, Большая Пироговская, "
            "дом 35б, кв. 6, телефон: 2-03-27, день рождения: 15.05.1891\n"
            "Владимир Маяковский — адрес: Россия, Москва, Лубянский проезд, "
            "д. 3, кв. 12, телефон: 73-88, день рождения: 19.07.1893"
        )
        # Проверяем output студента
        # Ожидаю 2 контакта, которые могут быть созданы и выведены в
        # относительно произвольном порядке порядке (вывод данных объекта
        # следует всегда после сообщения о его создании)

        # Ожидаемые строки
        cls.mike_create_info = "сообщение о создании контакта 'mike'"
        cls.vlad_create_info = "сообщение о создании контакта 'vlad'"
        cls.mike_print_info = "информация о контакте 'mike'"
        cls.vlad_print_info = "информация о контакте 'vlad'"
        cls.info = {
            cls.mike_create_info: "Создаём новый контакт Михаил Булгаков",
            cls.vlad_create_info: "Создаём новый контакт Владимир Маяковский",
            cls.mike_print_info: (
                "Михаил Булгаков — "
                "адрес: Россия, Москва, Большая Пироговская, дом 35б, кв. 6, "
                "телефон: 2-03-27, день рождения: 15.05.1891"
            ),
            cls.vlad_print_info: (
                "Владимир Маяковский — "
                "адрес: Россия, Москва, Лубянский проезд, д. 3, кв. 12, "
                "телефон: 73-88, день рождения: 19.07.1893"
            )
        }

    # Проверяем наличие ожидаемых строк в output студента
    def test_present_lines_count(self):
        # Должно выводиться 4 непустых строки
        should_be_lines_count = 4
        lines_count = self.output.count("\n") - self.output.count("\n\n") + 1
        assert (
            lines_count == should_be_lines_count
        ), f"Проверьте, что выводится {should_be_lines_count} строки."

    # Проверяем наличие ожидаемых строк в output студента
    def test_line_present(self):
        for key, value in self.info.items():
            assert (
                value in self.output
            ), (f"Проверьте, что корректно выводится {key}. Долно быть: "
                f"'\n{value}'.")

    # Проверяем порядок ожидаемых строк в output студента
    def test_mike_output_order(self):
        ind_mike_create_info = self.output.find(
            self.info.get(self.mike_create_info)
        )
        ind_mike_print_info = self.output.find(
            self.info.get(self.mike_print_info)
        )
        assert (
            ind_mike_create_info < ind_mike_print_info
        ), (f"{self.mike_print_info} выводится раньше, чем "
            f"{self.mike_create_info}")

    def test_vlad_output_order(self):
        ind_vlad_create_info = self.output.find(
            self.info.get(self.vlad_create_info)
        )
        ind_vlad_print_info = self.output.find(
            self.info.get(self.vlad_print_info)
        )
        assert (
            ind_vlad_create_info < ind_vlad_print_info
        ), (f"{self.vlad_print_info} выводится раньше, чем "
            f"{self.vlad_create_info}")


# Проверили правильность вывода, проверим реализацию метода show_contact.

# Наивный способ.
# Используем класс Contact созданный студентом. Создаем объект, вызываем
# метод show_contact.
class TestShowContact:
    @classmethod
    def setup_class(cls):
        # Создаем случайный контакт
        random_numeric = [str(randint(0, 100)) for _ in range(0, 4)]
        cls.name = "name" + random_numeric[0]
        cls.phone = "phone" + random_numeric[1]
        cls.birthday = "birthday" + random_numeric[2]
        cls.address = "address" + random_numeric[3]
        cls.some_contact = StudentContact(
            name=cls.name,
            phone=cls.phone,
            birthday=cls.birthday,
            address=cls.address
        )
        cls.print_info = (
            f"{cls.name} — адрес: {cls.address}, телефон: {cls.phone}, "
            f"день рождения: {cls.birthday}"
        )

    def test_show_contact(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.some_contact.show_contact()
        line = buffer.getvalue().strip()
        assert (
            line == self.print_info
        ), (
            "Проверьте функцию show_contact.\n"
            "Для некого случайного объекта типа Contact ожидался следующий "
            "вывод:\n"
            f"'{self.print_info}'\nполучено:\n'{line}'."
        )


# ----------------------------------------------------------------------------

# Более безопасный метод.
# Не знаю, как решен вопрос безопасности на платформе, поэтому реализовал
# еще и следующий вариант. Если решение студента изолируется от среды, то
# нижеследующий код не имеет смысла.
# Мы не можем доверять реализованному студентом классу и его методам.
# Требуется проверка метода show_contact.

class TestShowContact_:
    @classmethod
    def setup_class(cls):
        cls.user_code = TestOutput.user_code
        cls.code = ast.parse(cls.user_code)

        # Создаем случайный контакт
        random_numeric = [str(randint(0, 100)) for _ in range(0, 4)]
        cls.name = "name" + random_numeric[0]
        cls.phone = "phone" + random_numeric[1]
        cls.birthday = "birthday" + random_numeric[2]
        cls.address = "address" + random_numeric[3]

        # На основе написанного нами класса проведем проверку фун show_contact
        class OurContactClass(BaseContact):
            def show_contact(self):
                exec(cls.get_source_show_contact(cls))

        cls.some_contact = OurContactClass(
            name=cls.name,
            phone=cls.phone,
            birthday=cls.birthday,
            address=cls.address
        )
        cls.print_info = (
            f"{cls.name} — адрес: {cls.address}, телефон: {cls.phone}, "
            f"день рождения: {cls.birthday}"
        )

    def get_source_show_contact(self):
        for module_node in self.code.body:
            if (
                isinstance(module_node, ast.ClassDef)
                and module_node.name == "Contact"
            ):
                break
        assert (
            module_node.name == "Contact"
        ), "Отсутствует класс Contact."

        for class_node in module_node.body:
            if (
                isinstance(class_node, ast.FunctionDef)
                and class_node.name == "show_contact"
            ):
                break
        assert (
            class_node.name == "show_contact"
        ), "Отсутствует метод show_contact класса Contact."

        # Проверяем, что функция содержит, только одно выражение
        assert (
            len(class_node.body) == 1
        ), "Метод должен содержать только 1 функцию 'print'."
        # Проверяем, что функция является функцией 'print'
        assert (
            class_node.body[0].value.func.id == "print"
        ), "Метод не содеждит функцию 'print'."
        return ast.get_source_segment(self.user_code, class_node.body[0])

    def test_show_contact(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.some_contact.show_contact()
        line = buffer.getvalue().strip()
        assert (
            line == self.print_info
        ), (
            "Проверьте функцию show_contact.\n"
            "Для некого случайного объекта типа Contact ожидался следующий "
            "вывод:\n"
            f"'{self.print_info}'\nполучено:\n'{line}'."
        )
