import statistic
import table
inputConnect = input('Вакансии или статистика: ')
if __name__ == '__main__':
    if inputConnect == 'Статистика':
        statistic.main()
    if inputConnect == 'Вакансии':
        table.main()
