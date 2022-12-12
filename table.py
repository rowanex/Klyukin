import csv
import numbers
import os
import re
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
    3:'Опыт работы',
    4:'Премиум-вакания',
    5:'Компания',
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
    def __init__(self, name, description, key_skills, experience_id, premium, employer_name, salary, area_name,
                 published_at):
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
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency


class Table:
    def create_table(self):
        table = PrettyTable(dic_naming.values())
        table.hrules = 1
        table.max_width = 20
        table.align = "l"
        return table

    def fill_table(self, data_vacancies, table):
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
        if fields == '':
            headlines = list(dic_naming.values())
            headlines.insert(0, '№')
            return headlines
        else:
            headlines = fields.split(', ')
            headlines.insert(0, '№')
            return headlines

    def get_start_end(self, numbers, resultList):
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
    @staticmethod
    def final_check(file_name, filterName, option, optionReverse):
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
        if os.stat(file_name).st_size == 0:
            return 'Пустой файл'
        else:
            return file_name

    @staticmethod
    def check_reverse_sortedList(option):
        if option == '':
            return option
        if option == 'Да':
            return option
        if option == 'Нет':
            return option
        return 'Порядок сортировки задан некорректно'

    @staticmethod
    def check_sort_option(option):
        if option == '':
            return ''
        if option in dic_naming.values():
            return option
        else:
            return 'Параметр сортировки некорректен'

    @staticmethod
    def get_filter(filters):
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
        if "T" in row and ":" in row:
            row = row.split('T')
            row = row[0]
            row = row.replace('-', '.')
            row = row.split('.')
            data = f'{row[-1]}.{row[-2]}.{row[-3]}'
            return data
        else:
            return row


    @staticmethod
    def get_filtered_vacancy(vacancies, filter_name, filter_value):
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
        return len(vacancy.key_skills)

    @staticmethod
    def currency_transfer(averageSalary, currency):
        return averageSalary * currency_to_rub[currency]

    @staticmethod
    def get_average_salary(vacancy):
        salary_from = float(vacancy.salary.salary_from)
        salary_to = float(vacancy.salary.salary_to)
        currency = vacancy.salary.salary_currency
        averageSalary = (salary_from + salary_to) / 2
        return InputConect.currency_transfer(averageSalary, currency)

    @staticmethod
    def get_times(vacancy):
        return vacancy.published_at

    @staticmethod
    def get_experience_info(vacancy):
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
        return vacancy.name

    @staticmethod
    def get_descriptions_vacancy(vacancy):
        return vacancy.description

    @staticmethod
    def is_premium_vacancy(vacancy):
        return dic_true_false[vacancy.premium]

    @staticmethod
    def get_employer_name(vacancy):
        return vacancy.employer_name

    @staticmethod
    def get_area_name(vacancy):
        return vacancy.area_name

    @staticmethod
    def get_sorted_vacancy(vacancies, option, is_reverse_option):
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
        return '{0:,}'.format(int(float(number))).replace(',', ' ')


    @staticmethod
    def formatter_to_100_Syblos(vacancies):
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
        file_name, filter_name, filter_value, option, is_reverse_option, vacancy_count, headlines = InputConect().get_input_parameters()
        #var_dump.var_dump(DataSet(file_name))
        data_set = DataSet(file_name)
        InputConect.print_table(data_set.vacancies_objects, filter_name, filter_value, option, is_reverse_option,
                                vacancy_count, headlines)



class DataSet:
    def __init__(self, file_name):
        self.file_name = file_name
        self.vacancies_objects = DataSet.parser_csv(file_name)

    @staticmethod
    def csv_filer(reader, list_naming):
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
                    resultList[i][j] = re.sub('<.*?>', '', resultList[i][j]).replace("    ", " ").replace("  ", " ").replace("  ", " ").replace(
                        "  ", " ").rstrip().lstrip().replace("  ", " ").replace(" ", " ")
                tempList.append(resultList[i][j])
            resultList[i] = tempList

        return resultList

    @staticmethod
    def reader_csv(file_name):
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
        vacancies_list = []
        if result_list:
            for row in result_list:
                dict = {}
                for i in range(len(row)):
                    dict[title_list[i]] = row[i]
                vacancies_list.append(
                    Vacancy(dict['name'], dict['description'], dict['key_skills'], dict['experience_id'], dict['premium'],
                            dict['employer_name'],
                            Salary(dict['salary_from'], dict['salary_to'], dict['salary_gross'], dict['salary_currency']),
                            dict['area_name'], dict['published_at']))
            return vacancies_list

        else:
            return vacancies_list


    @staticmethod
    def parser_csv(file_name):
        data_list, title_list = DataSet.reader_csv(file_name)
        result_list = DataSet.csv_filer(data_list, title_list)
        vacancies_list = DataSet.get_vacancies_list(result_list, title_list)
        return vacancies_list

def main():
    InputConect().start()


