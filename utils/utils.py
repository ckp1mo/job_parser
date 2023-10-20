from pathlib import Path


VACANCY_FILE = Path(Path.cwd(), 'output_files', 'vacancy.json')


def get_from_api(xx_request_api, xx_vacancy, search_query):
    """
    Функция создает экземпляры для работы с классом xx_RequestApi и xx_Vacancy. Далее у экземпляров вызываются методы
    xx_array - будущий список вакансий.
    :param search_query: передается поисковой запрос
    :param xx_request_api: передается класс для работы с API, где "хх" в имени подразумевает имя класса
    для работы с платформой
    :param xx_vacancy: передается класс для работы с массивом, где "хх" в имени подразумевает имя класса
    для работы с платформой
    :return: возвращает список вакансий -> list
    """
    #
    request_api = xx_request_api(search_query)
    xx_array = xx_vacancy(request_api.get_vacancies()).vacancy_to_list()
    return xx_array


def vacancy_filter(filter_words, vacancy_list):
    """
    Функция для фильтрации вакансий по ключевым словам
    :param filter_words: список слов для фильтрации: list
    :param vacancy_list: список экземпляров класса Vacancy: list
    :return: возвращает отфильтрованный список вакансий -> list
    """
    filtered_vacancy = []
    for copy in vacancy_list:
        for key in filter_words:
            if key.lower() in copy.vacancy.lower() or key.lower() in copy.description.lower():
                filtered_vacancy.append(copy)
                break
    return filtered_vacancy


def sort_vacancy_by_salary(vacancy_list, is_reverse):
    """
    Функция для сортировки вакансий по зарплате
    :param is_reverse: булевое значение указывает будет ли использована реверсивная сортировка: bool
    :param vacancy_list: список экземпляров класса Vacancy: list
    :return: отсортированный список вакансий -> list
    """
    sort_vacancy = sorted(vacancy_list, key=lambda x: x.salary, reverse=is_reverse)
    return sort_vacancy


def get_top_vacancies(vacancy_list, top_n):
    """
    Функция создает список вакансий длинной равной top_n
    :param vacancy_list: список экземпляров класса Vacancy: list
    :param top_n: число вакансий для вывода в топ: int
    :return: Возвращает список экземпляров класса Vacancy: list, в колличестве равное top_n
    """
    top_vacancy = []
    for num, vacancy in enumerate(vacancy_list, start=1):
        top_vacancy.append(vacancy)
        if num == top_n:
            break
    return top_vacancy
