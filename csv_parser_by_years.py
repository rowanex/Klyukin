import csv
import os

class DataSet:
    """ Класс для создания датасета с полученными вакансиями из csv файла """

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
    def filter_csv(data_list, header_list):
        """ Функция фильтрует вакансии в csv файле от пустых вакансий
        Attributes:
            data_list (list): Лист с вакансиями из csv файла
            header_list (list): Лист с заголовками полей вакансий
        Return:
            list: Лист с данными вакансий
        """
        filtered_data = [vacancy for vacancy in data_list]
        return filtered_data



class SplitCsvFile:

    @staticmethod
    def split_csv(file_name):
        """
        Разделяет файл CSV на несколько по годам.
        Attributes:
            file_name(str): Название csv файла с данными
        """
        data_list, header_list = DataSet().reader_csv(file_name)
        result_data = DataSet().filter_csv(data_list, header_list)
        for vacancy in result_data:
            year = vacancy[header_list.index('published_at')][:4]
            if os.path.exists(f"data/{year}.csv"):
                with open(f"data/{year}.csv", mode="a", encoding='utf-8-sig') as file:
                    file_writer = csv.writer(file, delimiter=',', lineterminator="\r")
                    file_writer.writerow(vacancy)
            else:
                with open(f"data/{year}.csv", mode="w", encoding='utf-8-sig') as file:
                    file_writer = csv.writer(file, delimiter=',', lineterminator="\r")
                    file_writer.writerow(header_list)
                    file_writer.writerow(vacancy)


class InputConect:
    """Класс для получения названия файла csv для разделения по годам"""

    @staticmethod
    def check_file(file_name):
        """Функция проверяет файл на наличие информации

        Attributes:
            file_name(str): Имя файла с информацией о вакансифях
        """
        if os.stat(file_name).st_size == 0:
            print('Пустой файл')
            exit()
        else:
            return file_name

    @staticmethod
    def get_input_parameters():
        """Функция получает имя сsv файла

         :Returns
            file_name(str): название файла с информацией
        """
        print('Введите название файла:', end=' ')
        file_name = InputConect().check_file(input())
        return file_name

    @staticmethod
    def start():
        """ Функция обрабатывает файл и разделяет по годам в отдельные csv-файлы
        """
        file_name = InputConect().get_input_parameters()
        SplitCsvFile().split_csv(file_name)



def main():
    """ Функция запускает обработку csv файла и разделение данных по годам
    """
    InputConect().start()

if __name__ == '__main__':
    main()