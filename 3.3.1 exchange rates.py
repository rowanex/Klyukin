import json

import requests as requests

import csv
import glob
import multiprocessing
import os
import re
import pandas as pd
import xmltodict as xmltodict


class Vacancy:
    """Класс для представления вакансии
       Attributes:
           name (str): Название вакансии
           salary (int): Средняя зарплата
           area_name (str): Название региона
           published_at (str): Дата публикации вакансии
       """
    def __init__(self, name, salary, area_name, published_at):
        """Инициализирует объект Vacancy
        Args:
            name (str): Название вакансии
            salary (str or int or float): Средняя зарплата
            area_name (str): Название региона
            published_at (str): Дата публикации вакансии
        """
        self.name = name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


class Salary:
    """ Класс для представления зарплаты
    Attributes:
        salary_from (int): Нижняя граница вилки оклада
        salary_to (int): Верхняя граница вилки оклада
        salary_currency (str): Идентификатор валюты оклада
    """
    def __init__(self, salary_from, salary_to, salary_currency):
        """ Инициализирует объект Salary.
        Args:
            salary_from (str or int or float): Нижняя граница вилки оклада
            salary_to (str or int or float): Верхняя граница вилки оклада
            salary_currency (str): Идентификатор валюты оклада
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency


class DataSet:
    """ Класс для создания датасета с полученными вакансиями из csv файла
    Attributes:
        vacancies_objects (list[list[str]]): Лист объектов вакансий
    """
    def __init__(self, file_name):
        """ Инициализирует объект DataSet, для работы получает название csv файла, с которым мы работаем
        Args:
             file_name (str): Название файла со статистикой
        """
        self.file_name = file_name
        self.vacancies_objects = DataSet.parser_csv(file_name)

    @staticmethod
    def csv_filer(reader, list_naming):
        """Функция считывающая данные из csv файла статистических данных. Также чистит от html-тегов, пробелов
        Attributes:
            reader(list[list[str]]):  Исходные данные из csv файла (вакансии)
            list_naming(list[str]): Названия столбцов
        Returns:
             resultList(list[list[str]]): DataSet со всеми вакансиями
        """
        dataList, headerList = reader, list_naming
        if dataList == [] and headerList == []:
            resultList = []
            return resultList
        for i in range(len(dataList)):
            tempList = []
            for j in range(len(dataList[i])):
                if j == 2 and dataList[i][j]:
                    dataList[i][j] = dataList[i][j].split('\n')
                elif j == 2 and not dataList[i][j]:
                    dataList[i][j] = []
                else:
                    dataList[i][j] = re.sub('<.*?>', '', dataList[i][j]).replace("    ", " ").replace("  ",
                                                                                                          " ").replace(
                        "  ", " ").replace(
                        "  ", " ").rstrip().lstrip().replace("  ", " ").replace(" ", " ")
                tempList.append(dataList[i][j])
            dataList[i] = tempList
        return dataList

    @staticmethod
    def reader_csv(file_name):
        """ Функция читает CSV файл статистики и создает два list'a с данными и с заголовками файла csv
        Attributes:
            file_name (str): Имя файла CSV, из которого будут читаться данные
        Return:
            list: Лист с данными вакансий
            list: Лист с заголовками csv файла
        """
        with open(file_name, encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            dataList = list(reader)
            if dataList == []:
                headerList = dataList
                return dataList, headerList
            else:
                headerList = dataList[0]
                dataList.pop(0)
                return dataList, headerList

    @staticmethod
    def get_vacancies_list(result_list, title_list):
        """ Функция получает лист вакансий, состоящий из объектов Vacancy
        Attributes:
            result_list(list): Лист с данными о вакансиях
            title_list(list): Лист с заголовками
        Return:
            list: Лист вакансий с объектами вакансий
        """
        vacancies_list = []
        if result_list:
            for row in result_list:
                dict = {}
                for i in range(len(row)):
                    dict[title_list[i]] = row[i]
                vacancies_list.append(
                    Vacancy(dict['name'], Salary(dict['salary_from'], dict['salary_to'], dict['salary_currency']),
                            dict['area_name'], dict['published_at']))
            return vacancies_list
        else:
            return vacancies_list

    @staticmethod
    def parser_csv(file_name):
        """ Функция обрабатывает файл csv и получает лист вакансий с объектами вакансий
        Attributes:
            file_name(str): Название csv файла со статистикой
        Return:
            list: Лист вакансий с объектами вакансий
        """
        data_list, title_list = DataSet.reader_csv(file_name)
        result_list = DataSet.csv_filer(data_list, title_list)
        vacancies_list = DataSet.get_vacancies_list(result_list, title_list)
        return vacancies_list

def get_list_csv_files():
    """ Функция определяет в файловой системе лист файлов csv с которыми нужно работать анализируя данные
    Return:
        list[str]: лист названий csv файлов
    """
    path = r'C:\Users\Admin\PycharmProjects\Klyukin\data'
    os.chdir(path)
    files = glob.glob('*.{}'.format('csv'))
    return files

def get_frequency_for_currencies_by_file(file):
    """ Функуия находит частотность встречаемых валют в списке вакансий в определенном файле
        и возвращает словарь с названием и частотой
    Attributes:
        file(str): Файл с вакансиями
    Return:
        dict: Словарь - "RU":1000
    """
    vacancies_list = DataSet.parser_csv(file)
    dict_frequency = {}
    for vacancy in vacancies_list:
        if vacancy.salary.salary_currency not in dict_frequency:
            dict_frequency[vacancy.salary.salary_currency] = 1
        else:
            dict_frequency[vacancy.salary.salary_currency] += 1
    return dict_frequency

def get_frequency_for_currencies():
    """Функция находит частотность всех валют в данных с 2003 по 2022 год
    """
    csv_files = get_list_csv_files()
    with multiprocessing.Pool(processes=16) as p:
        result = p.map(get_frequency_for_currencies_by_file, csv_files)
    united_dict_frequency = {}
    for year in result:
        for currency in year:
            if currency not in united_dict_frequency:
                united_dict_frequency[currency] = year[currency]
            else:
                united_dict_frequency[currency] += year[currency]
    if '' in united_dict_frequency.keys():
        del united_dict_frequency['']
    return united_dict_frequency



def get_name_currency_for_dataframe(currency_frequency):
    """ Функция получает словарь с частотностью упоминаний валют и
        проводит выборку по количеству ваканисий с валютой, частотность которой > 5000
    Attributes:
        frequency(dict{}): словарь с наиболее валютами и их частотностью
    Return:
        list: Лист с названиями валют для dataframe
    """
    currency_for_df_dict = currency_frequency
    currencies_for_df_list = []
    for currency in currency_for_df_dict:
        if currency_for_df_dict[currency] >= 5000:
            currencies_for_df_list.append(currency)
    return currencies_for_df_list


def get_min_and_max_date(name_currency_for_dataframe):
    """ Функция находит минимальные и максимальные даты с вакансиями
    Attributes:
        currencies_for_dataframe(list[str]): Лист валют для dataframe
    Returns:
         str: минимальная дата
         str: максимальная дата
    """
    vacancy_dictionary_start = DataSet.parser_csv('2003.csv')
    vacancy_dictionary_final = DataSet.parser_csv('2022.csv')
    min_year = 2023
    min_month = 12
    for vacancy in vacancy_dictionary_start:
        if vacancy.salary.salary_currency in name_currency_for_dataframe:
            vacancy_year = int(vacancy.published_at[:4])
            vacancy_month = int(vacancy.published_at[5:7])
            if vacancy_year < min_year:
                min_year = vacancy_year
                min_month = vacancy_month
            if vacancy_year == min_year and min_month > vacancy_month:
                min_year = vacancy_year
                min_month = vacancy_month
    min_date = f'{min_year}-{min_month}'
    max_year = 2002
    max_month = 1
    for vacancy in vacancy_dictionary_final:
        if vacancy.salary.salary_currency in name_currency_for_dataframe:
            vacancy_year = int(vacancy.published_at[:4])
            vacancy_month = int(vacancy.published_at[5:7])
            if vacancy_year > max_year:
                max_year = vacancy_year
                max_month = vacancy_month
            if vacancy_year == max_year and max_month < vacancy_month:
                max_year = vacancy_year
                max_month = vacancy_month
    if max_month < 10:
        max_month = '0' + str(max_month)
    max_date = f'{max_year}-{max_month}'
    return min_date, max_date

def get_exchange_rates(min_date, max_date, name_currency_for_dataframe):
    """ Получает курсы валют помесячно с минимальной даты по максимальной в виде листа
    Attributes:
        min_date(str): минимальная дата
        max_date(str): максимальная дата
        name_currency_for_dataframe(list[str]): названия валют для dataframe
    Return:
        list[dict{str: str}]: Лист со словарями в которых курсы валют с датой
    """
    path = r'C:\Users\Admin\PycharmProjects\Klyukin'
    os.chdir(path)
    exchange_rates_by_date = []
    min_year = int(min_date[:4])
    max_year = int(max_date[:4])
    max_month = int(max_date[5:7])
    for i in range(min_year, max_year + 1):
        for j in range(1, 13):
            currency_by_date_dict = {}
            currency_by_date_dict['date'] = f'{i}-{j:02}'
            url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{j:02}/{i}'
            response = requests.get(url).text
            json_text = json.dumps(xmltodict.parse(response))
            currencies = eval(json_text)['ValCurs']['Valute']
            for currency in currencies:
                if currency['CharCode'] in name_currency_for_dataframe:
                    currency_by_date_dict[currency['CharCode']] = round(float(currency['Value'].replace(',', '.')) / float(currency['Nominal'].replace(',', '.')), 7)
            exchange_rates_by_date.append(currency_by_date_dict)
            if i == int(max_year) and j == max_month:
                break
    return exchange_rates_by_date


def get_dataframe(currencies_date):
    """ Функция получает лист с курсами валют и создает и сохраняет dataFrame
    Attributes:
        currencies_date(list[dict{str: str}]): Лист со словарями в которых курсы валют с датой
    """
    df = pd.DataFrame(currencies_date)
    df.to_csv('exchange_rates.csv', index=False)

def main():
    """ Функция иницирует сбор данных: о частотности валют, о валютах,
        частотность которых в вакансий > 5000, минимальной и максимальной датах, курсах валют
        и сохраняет dataframe
    """
    currency_frequency = get_frequency_for_currencies()
    print('Частотность всех валют: ', currency_frequency)
    name_currency_for_dataframe = get_name_currency_for_dataframe(currency_frequency)
    print('> 5000 раз:', name_currency_for_dataframe)
    min_date, max_date = get_min_and_max_date(name_currency_for_dataframe)
    currencies_date = get_exchange_rates(min_date, max_date, name_currency_for_dataframe)
    get_dataframe(currencies_date)

if __name__ == '__main__':
    main()