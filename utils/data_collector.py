from utils.data_verification import DataVerification


def data_collector():
    """
    Функция собирает данные от пользователя для уточнения запроса по вакансиям, сортировки, фильтрации.
    :return: возращает словарь с данными -> dict,
    search_query - ключ для API, поиска вакансий по этому значению -> str,
    top_n - колличество вакансий для вывода в консоль -> int,
    platforms - номер платформы из списка, при неккоректном вводе значение равно 3 -> str,
    platform_name - название выбранной платформы -> str
    is_filter - булевое значение, указывает, нужно ли фильтровать вакансии по словам -> bool,
    filter_words - спиоск слов для для фильтрации вакансий, при некорректном вводе список будет пустой -> list
    is_sort - булевое значение указывает, нужно ли сортировать вакансии по зарплате -> bool,
    is_reverse - булевое значение указывает реверсивную сортировку -> bool,
    text_reverse - строковое пояснение про вид соритровки -> str.
    """
    # Вызов метода класса DataVerification для получения ключа для поиска вакансий
    search_query = DataVerification().get_search_query()
    # Вызов метода класса DataVerification для получения колличества вывода вакансий
    top_n = DataVerification().get_top_n()

    # Вызов метода класса DataVerification для получения платформы для поиска вакансий, а так же имени ее
    platforms, platform_name = DataVerification().get_platform()

    # Вызов метода класса DataVerification для уточнения фильтрации вакансий по словам
    is_filter, filter_words = DataVerification().get_is_filter()

    # Вызов метода класса DataVerification для уточнения сортировки вакансий по зарплате
    is_sort, is_reverse, text_reverse = DataVerification().get_is_sort()

    return {'search_query': search_query,
            'top_n': top_n,
            'platforms': platforms,
            'platform_name': platform_name,
            'is_filter': is_filter,
            'filter_words': filter_words,
            'is_sort': is_sort,
            'is_reverse': is_reverse,
            'text_reverse': text_reverse
            }
