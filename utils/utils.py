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
