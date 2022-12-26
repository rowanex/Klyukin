import csv
import numbers
import os
import re
import cProfile
import datetime

from prettytable import PrettyTable

dic_naming = {
    'name': 'Название',
    'description': 'Описание',
    'key_skills': 'Навыки',
    'experience_id': 'Опыт работы',
    'premium': 'Премиум-вакансия',
    'employer_name': 'Компания',
    'salary': 'Оклад',
    'area_name': 'Название региона',
    'published_at': 'Дата публикации вакансии',
}

dic_naming_filter_helped = {
    'Название': 0,
    'Описание': 1,
    'Навыки': 2,
    'Опыт работы': 3,
    'Премиум-вакансия': 4,
    'Компания': 5,
    'Оклад': '6, 7, 8',
    'Идентификатор валюты оклада': 9,
    'Название региона': 10,
    'Дата публикации вакансии': 11
}

dic_naming_filter_helped_reversed = {
    0: 'Название',
    1: 'Описание',
    2: 'Навыки',
    3: 'Опыт работы',
    4: 'Премиум-вакания',
    5: 'Компания',
    '6, 7, 8': 'Оклад',
    9: 'Идентификатор валюты оклада',
    10: 'Название региона',
    11: 'Дата публикации вакансии'
}

dic_experience = {
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет"
}

dic_currency = {
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум",
}
currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}
dic_true_false = {
    'False': 'Нет',
    'True': 'Да',
    'FALSE': 'Нет',
    'TRUE': 'Да'
}
dic_salary_gross = {
    'Нет': 'С вычетом налогов',
    'Да': 'Без вычета налогов'
}


class Vacancy:
    """ Класс для представления вакансии

    """

    def __init__(self, name, description, key_skills, experience_id, premium, employer_name, salary, area_name,
                 published_at):
        """ Инициализирует объект Vacancy

        Args:
            name (str): Название вакансии
            description(str): Описание вакансии
            key_skills(str): Ключевые навыки
            experience_id(str): Опыт работы
            premium(bool): Премиум вакансия или нет
            employer_name(str): Название компании
            salary (str or int or float): Средняя зарплата
            area_name (str): Название региона
            published_at (str): Дата публикации вакансии
        """
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


class Salary:
    """ Класс для представления зарплаты

    Attributes:
        salary_from (int): Нижняя граница вилки оклада
        salary_to (int): Верхняя граница вилки оклада
        self.salary_gross(bool): До вычета налогов или нет
        salary_currency (str): Идентификатор валюты оклада
    """

    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        """
        Инициализирует объект Salary.
        Args:
            salary_from (int): Нижняя граница вилки оклада
            salary_to (int): Верхняя граница вилки оклада
            salary_gross(bool): До вычета налогов или нет
            salary_currency (str): Идентификатор валюты оклада
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency


class Table:
    """ Класс для создания таблицы и представления таблицы

    """

    def create_table(self):
        """ Функция создает таблицу с параметрами по ТЗ и возвращает её же
        Return:
            PrettyTable: Таблица
        """
        table = PrettyTable(dic_naming.values())
        table.hrules = 1
        table.max_width = 20
        table.align = "l"
        return table

    def fill_table(self, data_vacancies, table):
        """ Функция заполняет таблицу переданными в функцию данными о вакансиях
        Attributes:
            data_vacancies (list): Лист с данными о вакансиях
            table(PrettyTable): Пустая таблица
        Return:
            PrettyTable: Таблица заполненная данными
        """
        if data_vacancies == []:
            return ('Нет данных')
        for vacancy in data_vacancies:
            vac = []
            vac.append(vacancy.name)
            vac.append(vacancy.description)
            vac.append(vacancy.key_skills)
            vac.append(vacancy.experience_id)
            vac.append(vacancy.premium)
            vac.append(vacancy.employer_name)
            vac.append(vacancy.salary)
            vac.append(vacancy.area_name)
            vac.append(vacancy.published_at)
            table.add_row(vac)
        table.add_autoindex('№')
        return table

    def get_fields(self, fields):
        """ Функция обрабатывает поля для таблицы и возвращает их обработанными
        Attributes:
            fields (str): названия столбцов, информацию по которым нужно отобразить
        Return:
            list: Лист с данными о столбцах(названия)
        """
        if fields == '':
            headlines = list(dic_naming.values())
            headlines.insert(0, '№')
            return headlines
        else:
            headlines = fields.split(', ')
            headlines.insert(0, '№')
            return headlines

    def get_start_end(self, numbers, resultList):
        """ Функция обрабатывает первую и последнюю строку которую нужно отобразить в таблице
        Attributes:
            numbers (str): номера строк для отображения
            resultList (list): Лист с данными о вакансиях
        Return:
            int: 1 число(строка с которой надо отображать статистику)
            int: 2 число(до которой надо отображать статистику)
        """
        numbers = numbers.split(' ')
        if len(numbers) == 2:
            return int(numbers[0]) - 1, int(numbers[1]) - 1
        elif len(numbers) == 1:
            if numbers[0] == '':
                return 0, len(resultList)
            else:
                if int(numbers[0]) > 0:
                    return int(numbers[0]) - 1, len(resultList)
                else:
                    return int(numbers[0]), len(resultList)


class InputConect:
    """ Обрабатывает параметры, вводимые пользователями и печатает таблицу

    """

    @staticmethod
    def final_check(file_name, filterName, option, optionReverse):
        """ Функция проводит последнюю проверку на входные параметры и в случае ошибки завершает работу программы
        Attributes:
            file_name(str): Название файла csv со статистикой или "Пустой файл"
            filterName(str): Поля для фильтра или "Формат ввода некорректен"
            option(str): Параметр сортировки или "Параметр поиска некорректен"
            optionReverse(str): Порядок сортировки или 'Порядок сортировки задан некорректно'
        Return:
            str: Название файла csv со статистикой
            str: Поля для фильтра
            str: Параметр сортировки
            str: Порядок сортировки
        """
        if file_name == 'Пустой файл':
            print(file_name)
            exit()
        if filterName == 'Формат ввода некорректен':
            print(filterName)
            exit()
        if filterName == 'Параметр поиска некорректен':
            print(filterName)
            exit()
        if option == 'Параметр сортировки некорректен':
            print(option)
            exit()
        if optionReverse == 'Порядок сортировки задан некорректно':
            print(optionReverse)
            exit()
        return file_name, filterName, option, optionReverse

    @staticmethod
    def check_file(file_name):
        """ Функция проверяет не пустой ли csv файл со статистикой
        Attributes:
            file_name(str): Название файла csv со статистикой
        Return:
            str: Название файла csv со статистикой или "Пустой файл"
        """
        if os.stat(file_name).st_size == 0:
            return 'Пустой файл'
        else:
            return file_name

    @staticmethod
    def check_reverse_sortedList(option):
        """ Функция проверяет на правильность заданного порядка сортироваки
        Attributes:
            option(str): Порядок сортировки
        Return:
            str: Порядок сортировки или сообщение об ошибке('Порядок сортировки задан некорректно')
        """
        if option == '':
            return option
        if option == 'Да':
            return option
        if option == 'Нет':
            return option
        return 'Порядок сортировки задан некорректно'

    @staticmethod
    def check_sort_option(option):
        """ Функция проверяет на правильность заданного параметра сортировки
        Attributes:
            option(str): Параметр сортировки
        Return:
            str: Параметр сортировки или сообщение об ошибке('Параметр сортировки некорректен')
        """
        if option == '':
            return ''
        if option in dic_naming.values():
            return option
        else:
            return 'Параметр сортировки некорректен'

    @staticmethod
    def get_filter(filters):
        """ Функция возвращает обработанный параметр фильтра данных по вакансиям
        Attributes:
            filters(str): Параметр фильтрации
        Return:
            str: параметр фильтрации
            str: значение параметра фильтрации
        """
        if filters == '':
            return '', ''
        if ':' not in filters:
            return 'Формат ввода некорректен', ''
        filters = filters.split(':')
        if filters[0] not in dic_naming_filter_helped.keys():
            return 'Параметр поиска некорректен', ''
        if len(filters) == 2:
            filterName = filters[0]
            filterValue = filters[1]
            return filterName.strip(), filterValue.strip()
        else:
            return filters, ''

    @staticmethod
    def get_input_parameters():
        """ Функция получает данные для анализа данных по вакансиям
        Return:
            str: Название csv файла со статистикой
            str: Параметр фильтрации
            str: Значение параметра фильтрации
            str: Значение сортировки
            str: Значение порядка сортировки
            str: Диапазон вывода строк(вакансий)
            str: Требуемые столбцы для вывода в таблицу
        """
        print('Введите название файла:', end=' ')
        file_name = InputConect().check_file(input())
        print('Введите параметр фильтрации:', end=' ')
        filter_name, filter_value = InputConect().get_filter(input())
        print('Введите параметр сортировки:', end=' ')
        option = InputConect().check_sort_option(input())
        print('Обратный порядок сортировки (Да / Нет):', end=' ')
        is_reverse_option = InputConect().check_reverse_sortedList(input())
        print('Введите диапазон вывода:', end=' ')
        vacancy_count = input()
        print('Введите требуемые столбцы:', end=' ')
        headlines = input()
        checked_file_name, checked_filter_name, checked_option, checked_is_reverse_option = InputConect().final_check(
            file_name, filter_name, option,
            is_reverse_option)
        return checked_file_name, checked_filter_name, filter_value, checked_option, checked_is_reverse_option, vacancy_count, headlines

    @staticmethod
    def fix_published_time(row):
        """ Функция изменяет вид представления времени
        Attributes:
            row(str): дата публикации
        Return:
            str: обновленная дата публикации
        """
        if "T" in row and ":" in row:
            row = row.split('T')
            row = row[0]
            row = row.replace('-', '.')
            row = row.split('.')
            data = f'{row[-1]}.{row[-2]}.{row[-3]}'
            return data
        else:
            return row

    #@staticmethod
    #def fix_published_time_2(date):
        #result_date = datetime.datetime.strptime(date[:10], '%Y-%m-%d').date()
        #return '{0.day}.{0.month}.{0.year}'.format(result_date)

    #@staticmethod
    #def fix_published_time_3(date):
        #return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')


    @staticmethod
    def get_filtered_vacancy(vacancies, filter_name, filter_value):
        """ Функция работая с листом вакансий получает отфильтрованный лист вакансий
        Attributes:
            vacancies(list): лист с вакансиями
            filter_name(str): Параметр фильтрации
            filter_value(str): Значение параметра фильтрации
        Return:
            list: отфильтрованный лист вакансий
        """
        if filter_name == '':
            return vacancies
        if filter_name in dic_naming_filter_helped.keys():
            finalList = []
            filter_name_assistent = dic_naming_filter_helped.get(filter_name)
            if isinstance(filter_name_assistent, numbers.Number):
                if filter_name_assistent == 11:
                    for vacancy in vacancies:
                        if InputConect.fix_published_time(vacancy.published_at) == filter_value:
                            finalList.append(vacancy)
                        else:
                            pass
                elif filter_name_assistent == 2:
                    filter_value_list = filter_value.split(', ')
                    count = 0
                    for vacancy in vacancies:
                        for i in filter_value_list:
                            if i in vacancy.key_skills:
                                count += 1
                            if count == len(filter_value_list):
                                finalList.append(vacancy)
                        count = 0
                elif filter_name_assistent == 9:
                    for vacancy in vacancies:
                        salary = vacancy.salary
                        if dic_currency[salary.salary_currency] == filter_value:
                            finalList.append(vacancy)
                        else:
                            pass
                elif filter_name_assistent == 0:
                    for vacancy in vacancies:
                        if vacancy.name == filter_value:
                            finalList.append(vacancy)
                        else:
                            pass
                elif filter_name_assistent == 1:
                    for vacancy in vacancies:
                        if vacancy.description == filter_value:
                            finalList.append(vacancy)
                        else:
                            pass
                elif filter_name_assistent == 3:
                    for vacancy in vacancies:
                        if dic_experience[vacancy.experience_id] == filter_value:
                            finalList.append(vacancy)
                        else:
                            pass
                elif filter_name_assistent == 4:
                    for vacancy in vacancies:
                        if dic_true_false[vacancy.premium] == filter_value:
                            finalList.append(vacancy)
                        else:
                            pass
                elif filter_name_assistent == 5:
                    for vacancy in vacancies:
                        if vacancy.employer_name == filter_value:
                            finalList.append(vacancy)
                        else:
                            pass
                elif filter_name_assistent == 10:
                    for vacancy in vacancies:
                        if vacancy.area_name == filter_value:
                            finalList.append(vacancy)
                        else:
                            pass
            else:
                for vacancy in vacancies:
                    if float(vacancy.salary.salary_from) <= float(filter_value) <= float(vacancy.salary.salary_to):
                        finalList.append(vacancy)
                    else:
                        continue
            return finalList
        else:
            return 'Ошибка в фильтре'

    @staticmethod
    def count_key_skills(vacancy):
        """ Функция возвращает кол-во ключевых навыков
        Attributes:
            vacancy(object): объект вакансии
        Return:
            int: кол-во ключевых навыков
        """
        return len(vacancy.key_skills)

    @staticmethod
    def currency_transfer(averageSalary, currency):
        """Функция возвращает переведенную в рубли сумму
        Attributes:
            averageSalary(float): название файла с информацией
            currency(str): Идентификатор валюты оклада
        Returns:
            averageSalary * currency_to_rub[currency](float): переведенное значение суммы в рубли
        """
        return averageSalary * currency_to_rub[currency]

    @staticmethod
    def get_average_salary(vacancy):
        """Функция считает среднюю зарплату

        Attributes:
            vacancy(object): Имя файла картинки графиков
        Returns:
            currency_transfer(): возвращаем результат функции перевода в рубли
        """
        salary_from = float(vacancy.salary.salary_from)
        salary_to = float(vacancy.salary.salary_to)
        currency = vacancy.salary.salary_currency
        averageSalary = (salary_from + salary_to) / 2
        return InputConect.currency_transfer(averageSalary, currency)

    @staticmethod
    def get_times(vacancy):
        """ Функция возвращает время публикации вакансии
        Attributes:
            vacancy(object): объект вакансии
        Return:
            str: время публикации вакансии
        """
        return vacancy.published_at

    @staticmethod
    def get_experience_info(vacancy):
        """ Функция возвращает индекс опыта работы
        Attributes:
            vacancy(object): объект вакансии
        Return:
            int: индекс опыта работы
        """
        experience = dic_experience[vacancy.experience_id]
        if experience == 'Нет опыта':
            return 0
        if experience == 'От 1 года до 3 лет':
            return 1
        if experience == 'От 3 до 6 лет':
            return 2
        if experience == 'Более 6 лет':
            return 3

    @staticmethod
    def get_name_vacancy(vacancy):
        """ Функция возвращает название вакансии
        Attributes:
            vacancy(object): объект вакансии
        Return:
            str: название вакансии
        """
        return vacancy.name

    @staticmethod
    def get_descriptions_vacancy(vacancy):
        """ Функция возвращает краткое описание
        Attributes:
            vacancy(object): объект вакансии
        Return:
            str: краткое описание
        """
        return vacancy.description

    @staticmethod
    def is_premium_vacancy(vacancy):
        """ Функция возвращает обработанное сообщение о том премиум ли вакансия
        Attributes:
            vacancy(object): объект вакансии
        Return:
            str: сообщение о том премиум ли вакансия
        """
        return dic_true_false[vacancy.premium]

    @staticmethod
    def get_employer_name(vacancy):
        """ Функция возвращает имя работодателя(компании)
        Attributes:
            vacancy(object): объект вакансии
        Return:
            str: имя работодателя(компании)
        """
        return vacancy.employer_name

    @staticmethod
    def get_area_name(vacancy):
        """ Функция возвращает название региона вакансии
        Attributes:
            vacancy(object): объект вакансии
        Return:
            str: название региона вакансии
        """
        return vacancy.area_name

    @staticmethod
    def get_sorted_vacancy(vacancies, option, is_reverse_option):
        """ Функция работая с листом вакансии получает отсортированный по параметру сортировки лист с вакансиями
        Attributes:
            vacancies(object): объект вакансии
            option(str): Параметр сортировки
            is_reverse_option(str): Параметр порядка сортировки
        Return:
            list: отсортированный по параметру сортировки лист с вакансиями
        """
        if option == '':
            return vacancies
        else:
            if option == 'Навыки':
                return sorted(vacancies, key=InputConect.count_key_skills, reverse=is_reverse_option == 'Да')
            if option == 'Оклад':
                return sorted(vacancies, key=InputConect.get_average_salary, reverse=is_reverse_option == 'Да')
            if option == 'Дата публикации вакансии':
                return sorted(vacancies, key=InputConect.get_times, reverse=is_reverse_option == 'Да')
            if option == 'Опыт работы':
                return sorted(vacancies, key=InputConect.get_experience_info, reverse=is_reverse_option == 'Да')
            if option == 'Название':
                return sorted(vacancies, key=InputConect.get_name_vacancy, reverse=is_reverse_option == 'Да')
            if option == 'Описание':
                return sorted(vacancies, key=InputConect.get_descriptions_vacancy, reverse=is_reverse_option == 'Да')
            if option == 'Премиум-вакансия':
                return sorted(vacancies, key=InputConect.is_premium_vacancy, reverse=is_reverse_option == 'Да')
            if option == 'Компания':
                return sorted(vacancies, key=InputConect.get_employer_name, reverse=is_reverse_option == 'Да')
            if option == 'Название региона':
                return sorted(vacancies, key=InputConect.get_area_name, reverse=is_reverse_option == 'Да')

    @staticmethod
    def create_space(number):
        """ Функция создает пробелы в числах между разрядами
        Attributes:
            number(int): число зп
        Return:
            str: число с пробелами между разрядами по ТЗ
        """
        return '{0:,}'.format(int(float(number))).replace(',', ' ')

    @staticmethod
    def formatter_to_100_Syblos(vacancies):
        """ Функция обрезает текст до 100 символов
        Attributes:
            vacancies(list): лист с объъектами вакансий
        Return:
            list: лист с объъектами вакансий, с текстом в полях объекта вакансий обрезанный до 100 символов
        """
        for vacancy in vacancies:
            key_skills = " ;; ".join(vacancy.key_skills)
            key_skills = key_skills.replace(" ;; ", '\n')
            description = vacancy.description
            for j in range(0, len(key_skills)):
                if len(key_skills) > 100:
                    key_skills = (key_skills[:100] + '...')
            vacancy.key_skills = key_skills
            for j in range(0, len(description)):
                if len(description) > 100:
                    description = (description[:100] + '...')
            vacancy.description = description
        return vacancies

    @staticmethod
    def formatter(vacancies):
        """ Функция форматирует объекты вакансий согласно ТЗ
        Attributes:
            vacancies(list): лист с объъектами вакансий
        Return:
            list: лист с объъектами вакансий, отформатированный согласно ТЗ
        """
        for vacancy in vacancies:
            vacancy.published_at = InputConect.fix_published_time(vacancy.published_at)
            vacancy.premium = dic_true_false.get(vacancy.premium)
            vacancy.experience_id = dic_experience[vacancy.experience_id]
            salary = vacancy.salary
            salary_from = salary.salary_from
            salary_to = salary.salary_to
            salary_currency = salary.salary_currency
            salary_gross = salary.salary_gross
            vacancy.salary = f'{InputConect.create_space(salary_from)} - {InputConect.create_space(salary_to)} ({dic_currency[salary_currency]}) ({dic_salary_gross[dic_true_false[salary_gross]]})'
        vacancies = InputConect.formatter_to_100_Syblos(vacancies)
        return vacancies

    @staticmethod
    def print_table(vacancies, filter_name, filter_value, option, is_reverse_option, vacancy_count, headlines):
        """ Функция форматирует объекты вакансий согласно ТЗ
            Attributes:
                    vacancies(list): лист с объъектами вакансий
                    filter_name(str): Параметр фильтрации
                    filter_value(str): Значение параметра фильтрации
                    option(str): Параметр сортировки
                    is_reverse_option(str): Параметр порядка сортировки
                    vacancy_count(str): Кол-во вакансий
                    headlines(str): Требуемиые столбцы

                """
        if len(vacancies) != 0:
            filtered_vacancies = InputConect.get_filtered_vacancy(vacancies, filter_name, filter_value)
            if filtered_vacancies != []:
                sorted_vacancies = InputConect.get_sorted_vacancy(filtered_vacancies, option, is_reverse_option)
                result_vacancies = InputConect.formatter(sorted_vacancies)
                analitic_table = Table().create_table()
                analitic_table = Table().fill_table(result_vacancies, analitic_table)
                starts, ends = Table().get_start_end(vacancy_count, result_vacancies)
                headlines = Table().get_fields(headlines)
                print(analitic_table.get_string(start=starts, end=ends, fields=headlines))
            else:
                print('Ничего не найдено')

        else:
            print('Нет данных')
            exit()

    @staticmethod
    def start():
        """Функция запускающая получение статистики и печати таблицы по параметрам
        """
        file_name, filter_name, filter_value, option, is_reverse_option, vacancy_count, headlines = InputConect().get_input_parameters()
        data_set = DataSet(file_name)
        InputConect.print_table(data_set.vacancies_objects, filter_name, filter_value, option, is_reverse_option,
                                vacancy_count, headlines)


class DataSet:
    """ Класс для создания датасета с полученными вакансиями из csv файла
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
        """Функция считывающая данные из csv файла статистических данных. Также чистит от html-тегов, пробелов и None'ов
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
            if '' in dataList[i] or len(dataList[i]) < len(headerList):
                dataList[i].clear()
        resultList = list(filter(None, dataList))
        for i in range(len(resultList)):
            tempList = []
            for j in range(len(resultList[i])):
                if j == 2 and resultList[i][j]:
                    resultList[i][j] = resultList[i][j].split('\n')

                elif j == 2 and not resultList[i][j]:
                    resultList[i][j] = []
                else:
                    resultList[i][j] = re.sub('<.*?>', '', resultList[i][j]).replace("    ", " ").replace("  ",
                                                                                                          " ").replace(
                        "  ", " ").replace(
                        "  ", " ").rstrip().lstrip().replace("  ", " ").replace(" ", " ")
                tempList.append(resultList[i][j])
            resultList[i] = tempList

        return resultList

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
                    Vacancy(dict['name'], dict['description'], dict['key_skills'], dict['experience_id'],
                            dict['premium'],
                            dict['employer_name'],
                            Salary(dict['salary_from'], dict['salary_to'], dict['salary_gross'],
                                   dict['salary_currency']),
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


def main():
    """ Функция запускает обработку данных и получает обработанные данные в виде таблицы
    """
    InputConect().start()


cProfile.run('main()')
