#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от полусуммы крайних значений цены за торговую сессию:
#   полусумма = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / полусумма) * 100%
# Например для бумаги №1:
#   half_sum = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / half_sum) * 100 = 8.7%
# Для бумаги №2:
#   half_sum = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / half_sum) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
import os
from operator import itemgetter
from collections import OrderedDict


def data_file(name_folder_in=None):
    for dirpath, dirnames, filenames in os.walk(os.path.normpath(name_folder_in)):  # Добываем названия всех файлов
        for file_name in filenames:
            full_file_path = os.path.join(dirpath, file_name)  # Получаем путь до каждого файла
            tickers_path.append(full_file_path)


class TickerVolatility:

    def __init__(self, path_file, *args, **kwargs):
        self.path_file = path_file  # Нормализируем путь до папки (для разных ОС)

    def run(self):
        with open(self.path_file, 'r', encoding='cp1251') as file:  # Читаем содержание файла
            next(file)  # Пропускаем строку с названиями столбцов
            line = next(file)  # Пеерходим ко второй строке
            line = line.split(',')  # Удаляем знак переноса строки и приводим к рабочему виду
            secid, tradetime, price, quantity = line  # Разбиваем на составляющие
            max_price = float(price)  # Создаем макс прайс
            min_price = float(price)  # Создаем мин прайс

            for line in file:  # построчно ищем мин и макс прайсы
                price = line.split(',')[2]  # Удаляем знак переноса строки и приводим к рабочему виду
                if float(price) > max_price:  # проверяем макс прайс
                    max_price = float(price)
                if float(price) < min_price:  # проверяем мин прайс
                    min_price = float(price)

        # После сбора максимальных и минимальных прайсов, переходим к вычислению волатильности
        half_sum = (max_price + min_price) / 2
        volatility = ((max_price - min_price) / half_sum) * 100
        if volatility == 0:  # если нулевая
            zero_secid[secid] = 0  # сохраняем в словарь нулевых волатильностей
        else:  # если не нулевая
            not_zero_secid[secid] = round(volatility, 2)  # сохраняем в словарь не нулевых волатильностей


tickers_path = []  # список путей до файла
not_zero_secid = OrderedDict()  # словарь сделок с НЕ НУЛЕВОЙ волатильностью
zero_secid = {}  # словарь сделок с НУЛЕВОЙ волатильностью

data_file(name_folder_in='trades')
for file in tickers_path:
    arrange = TickerVolatility(path_file=file)
    arrange.run()


# Реализуем вывод нужной информации
sort = sorted(not_zero_secid.items(), key=itemgetter(1))

print('Максимальная волатильность: ')
for secid_max_print in reversed(sort[-3:]):
    print(list(secid_max_print)[0], ' - ', list(secid_max_print)[1], '%')
print('Минимальная волатильность: ')
for secid_min_print in sort[0:3]:
    print(list(secid_min_print)[0], ' - ', list(secid_min_print)[1], '%')
print('Нулевая волатильность: ')
for secid_zero_print in zero_secid.items():
    print(list(secid_zero_print)[0], end=' ')

# Зачёт!
