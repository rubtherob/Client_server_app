"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

str_a = 'разработка'
str_b = 'администрирование'
str_c = 'protocol'
str_d = 'standard'

list = [str_a, str_b, str_c, str_d]

for el in list:
    el = el.encode()
    print(el)
    el = el.decode()
    print(el)
    print('-------')