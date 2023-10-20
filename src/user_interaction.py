from utils.utils import get_from_api, vacancy_filter, sort_vacancy_by_salary, get_top_vacancies
from utils.print_info import PrintInfo
from utils.data_collector import data_collector
from utils.data_verification import DataVerification
from src.hh_api import HHRequestApi, HHVacancy
from src.sj_api import SJRequestApi, SJVacancy
from src.vacancy import Vacancy, JSONSaver, VacancyOptions
from pathlib import Path
import json


VACANCY_FILE = Path(Path.cwd(), 'output_files', 'vacancy.json')


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

    # В блоке ниже вызывается функция get_from_api, а для all_vacancy присваивается массив с вакансиями
    if data_collection['platforms'] == "1":
        all_vacancy = get_from_api(HHRequestApi, HHVacancy, data_collection['search_query'])
    elif data_collection['platforms'] == "2":
        all_vacancy = get_from_api(SJRequestApi, SJVacancy, data_collection['search_query'])
    elif data_collection['platforms'] == '3':
        all_vacancy = get_from_api(HHRequestApi, HHVacancy, data_collection['search_query']) + \
                      get_from_api(SJRequestApi, SJVacancy, data_collection['search_query'])
    else:
        all_vacancy = get_from_api(HHRequestApi, HHVacancy, data_collection['search_query']) + \
                      get_from_api(SJRequestApi, SJVacancy, data_collection['search_query'])

    # Создание экземпляров вакансий на основе запроса методом класса Vacancy
    Vacancy.vacancy_to_instance(all_vacancy)
    # Список всех созданных экземпляров класса Vacancy
    vacancy_list = Vacancy.all

    # Выполняем пожелания пользователя. Фильтрацию, сортировку.
    if data_collection['is_filter']:
        # Вызываем функцию для выполнения фильтрации по заданным ключам
        vacancy_list = vacancy_filter(data_collection['filter_words'], Vacancy.all)
    if data_collection['is_sort']:
        # вызываем функцию для сортировки по зарплате
        vacancy_list = sort_vacancy_by_salary(vacancy_list, data_collection['is_reverse'])

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
        # Удаление файла с прошлых запросов, а почему бы и нет)
        if VACANCY_FILE.exists():
            VACANCY_FILE.unlink()
        # Вызов метод класса JSONSaver для сохранения топ списка вакансий в файл по пути /output_files/vacancy.json
        JSONSaver().save_vacancy(top_vacancy)
        print('Вакансии сохранены, ищи их в рабочей директори по пути /output_files/vacancy.json')
        print('Хорошего дня! :)')


def get_started():
    print('Хмм.. так-так, что-то там лежит в той коробочке..')
    start_data = input('Искать в прошлом поисковом запросе или начнем новый?'
                       '\n1. Искать в прошлом поиске'
                       '\n2. Начать новый поиск\n'
                       )
    if start_data == '1':
        user_choice = input('Посмотреть список вакансий или сразу поищем по ключевым словам?'
                            '\n1. Посмотреть'
                            '\n2. Искать\n'
                            )
        if user_choice == '1':
            try:
                with open(VACANCY_FILE, 'r', encoding='utf-8') as f:
                    PrintInfo().print_vacancy(json.load(f))
                    return True
            except json.JSONDecodeError:
                print('Файл испорчен')
                print('Запускаю новый поиск')
            except TypeError:
                print('Неккоректный формат вакансий')
                print('Запускаю новый поиск')
        elif user_choice == '2':
            return True
        else:
            print('И так сойдет')
            return False
    elif start_data == '2':
        return False
    else:
        print('И так сойдет')
        return False