import os
from datetime import datetime
from functools import wraps

# _______________________________________________________________________________________________
# Задача 1. Доработать декоратор. Должен получиться декоратор,
# который записывает в файл 'main.log' дату и время вызова функции,
# имя функции, аргументы, с которыми вызвалась, и возвращаемое значение.

def logger(old_function):
    @wraps(old_function)
    def new_function(*args, **kwargs):

        # Код до вызова исходной функции
        func_call_time = datetime.now()
        result = old_function(*args, **kwargs)
        # Код после вызова исходной функции
        with open('main.log', 'a', encoding='windows-1251') as file:
            file.write('_' * 70)
            file.write('\n')
            file.write(f'Дата и время вызова функции: {func_call_time}\n')
            file.write(f'Имя функции: {old_function.__name__}\n')
            file.write(f'Вызвана функция с аргументами: {args} и {kwargs}\n')
            file.write(f'Результат вызова функции: {result}\n')
            file.write('\n')
            print(f'После вызова функции {old_function.__name__} данные успешно записаны в файл "main/log"')

        return result

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()


# _______________________________________________________________________________________________
#  Задача 2. Доработать параметризованный декоратор logger в коде ниже.
#  Должен получиться декоратор, который записывает в файл дату и время вызова функции,
#  имя функции, аргументы, с которыми вызвалась, и возвращаемое значение.
#  Путь к файлу должен передаваться в аргументах декоратора.

def logger2(path):
    def __logger2(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            # Код до вызова исходной функции
            func_call_time = datetime.now()
            result = old_function(*args, **kwargs)
            # Код после вызова исходной функции
            with open(path, 'a', encoding='cp1251') as file:
                file.write('_' * 70)
                file.write('\n')
                file.write(f'Дата и время вызова функции: {func_call_time}\n')
                file.write(f'Имя функции: {old_function.__name__}\n')
                file.write(f'Вызвана функция с аргументами: {args} и {kwargs}\n')
                file.write(f'Результат вызова функции: {result}\n')
                file.write('\n')
                print(f'После вызова функции {old_function.__name__} данные успешно записаны в файл {path}')

            return result

        return new_function

    return __logger2


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger2(path)
        def hello_world():
            return 'Hello World'

        @logger2(path)
        def summator(a, b=0):
            return a + b

        @logger2(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()

# Задача 3. Применить написанный логгер к приложению из любого предыдущего д/з.

# # Задача из предыдущего ДЗ. Доработать функцию flat_generator. Должен получиться генератор, который принимает список списков
# # и возвращает их плоское представление.Функция test в коде ниже также должна отработать без ошибок.

import types

# Создаем функцию, проходящую по каждому значению каждого списка, вложенного в список списков
def flat_generator(list_of_lists):
    for item in list_of_lists:
        for value in item:
            yield value

# Создаем функцию - тест для определения корректности работы итератора, применяем к ней декоратор logger2
@logger2('log_4.log')
def test_3():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)

    return 'Функция вызвана успешно'

# Запускаем тестовую функцию
if __name__ == '__main__':
    test_3()
