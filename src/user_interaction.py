from utils.utils import vacancy_filter, get_top_vacancies
from utils.print_info import PrintInfo
from utils.data_collector import data_collector
from utils.data_verification import DataVerification
from src.platforms_request_api import PlatformsRequestApi
from src.vacancy import Vacancy, JSONSaver, VacancyOptions


def user_interaction():
    """
    Главная функция для запуска основного алгоритма поиска вакансий и сохранения результата в файл.
    :return: None
    """
    # Стартуем..
    print('Я немножко умею искать вакансии, поищем-ка :)')
    # вызов функции для сбора дополнительных параметров от пользователя (сортировка, фильтр по словам и тд)
    data_collection = data_collector()
    print('\nСекундочку..\n')

    # В блоке ниже матрешка. Вызывается классметод класса Vacancy, в него передается ответ сервера.
    # Который возвращается при вызове метода класса PlatformsRequestApi, с переданным ключем запроса в экземпляр
    if data_collection['platforms'] == "1":
        Vacancy.vacancy_to_list_hh(PlatformsRequestApi(data_collection['search_query']).get_vacancies_hh())
    elif data_collection['platforms'] == "2":
        Vacancy.vacancy_to_list_sj(PlatformsRequestApi(data_collection['search_query']).get_vacancies_sj())
    elif data_collection['platforms'] == '3':
        Vacancy.vacancy_to_list_hh(PlatformsRequestApi(data_collection['search_query']).get_vacancies_hh())
        Vacancy.vacancy_to_list_sj(PlatformsRequestApi(data_collection['search_query']).get_vacancies_sj())
    else:
        Vacancy.vacancy_to_list_hh(PlatformsRequestApi(data_collection['search_query']).get_vacancies_hh())
        Vacancy.vacancy_to_list_sj(PlatformsRequestApi(data_collection['search_query']).get_vacancies_sj())

    # Список всех созданных экземпляров класса Vacancy
    vacancy_list = Vacancy.all

    # Выполняем пожелания пользователя. Фильтрацию, сортировку.
    if data_collection['is_filter']:
        # Вызываем функцию для выполнения фильтрации по заданным ключам
        vacancy_list = vacancy_filter(data_collection['filter_words'], Vacancy.all)
    # Запускаем сортировку по выбранным параметрам
    if data_collection['is_sort']:
        if data_collection['is_reverse']:
            vacancy_list = sorted(vacancy_list, reverse=True)
        else:
            vacancy_list = sorted(vacancy_list, reverse=False)

    # вызов функции для отображения параметров поискового запроса
    PrintInfo().print_options(data_collection)
    input('\nДля продолжения нажмите "enter": ')
    # Вызываем функцию для получения колличества вакансий равной значению top_n
    top_vacancy = get_top_vacancies(vacancy_list, data_collection['top_n'])
    # Вызываем функцию для отображения списка наших вакансий в консоль
    PrintInfo().print_vacancy(top_vacancy)

    # Вызываем функцию с предложением удалить что-то из списка
    is_del = DataVerification().get_data_for_del()
    # Если значение is_del = True, тогда вызываем функцию для визуальной работы со списком вакансий
    if is_del:
        PrintInfo().print_for_del(top_vacancy, VacancyOptions, Vacancy)
    # Если список вакансий пуст. Вызываем функцию, которая сообщит о пустом списке и предложит начать поиск сначала
    if len(top_vacancy) == 0:
        PrintInfo().print_if_vacancy_list_empty(user_interaction)
    else:
        # Вызов метод класса JSONSaver для сохранения топ списка вакансий в файл по пути /output_files/{file_name}.json
        file_name = JSONSaver().get_file_name()
        JSONSaver().save_vacancy(top_vacancy, file_name)
        print(f'>> Вакансии сохранены, ищи их в рабочей директори по пути /output_files/{file_name}.json')
        print('>> Хорошего дня! :)')


def get_started(file_list):
    """
    Функция запускается при условии, что есть JSON файлы  в директории 'output_files'
    :param file_list: список с названиями файлов в директории 'output_files'
    :return: имя файла или None
    """
    print('Хмм.. так-так, что-то там лежит в той коробочке..')
    start_data = input('Искать в прошлом поисковом запросе или начнем новый?'
                       '\n1. Искать в прошлом поиске'
                       '\n2. Начать новый поиск\n'
                       )
    if start_data == '1':
        print('В каком файле будем искать?')
        while True:
            for i, file in enumerate(file_list, start=1):
                print(f'{i} - {file}')
            try:
                user_choice = int(input('Введите номер\n'))
                if user_choice == 0:
                    print('>> По такому номеру нет файла')
                    continue
                return file_list[user_choice-1]
            except ValueError:
                print('>> Нужно ввести цифру')
            except IndexError:
                print('>> По такому номеру нет файла')
    else:
        print('>> Запущен новый поиск')
