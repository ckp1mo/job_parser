from src.vacancy import Vacancy


class PrintInfo:
    """
    Класс печати информации в консоль.
    В частности работа со списком вакансий и параметрами поиска
    """
    @staticmethod
    def print_vacancy(top_vacancy):
        """
        Метод выводит в консоль номер и вакансию в удобном виде.
        Принимает список со словарями или список с экземплярами.
        :param top_vacancy: список с вакансиями: list
        :return: None
        """
        try:
            if isinstance(top_vacancy[0], Vacancy):
                print('-' * 108)
                for num, vacancy in enumerate(top_vacancy, start=1):
                    print(f'{num} - {vacancy}')
                print('-' * 108)
            elif type(top_vacancy[0]) == dict:
                print('-' * 108)
                for num, vacancy in enumerate(top_vacancy, start=1):
                    print(f'{num} - {vacancy["vacancy"]}, {vacancy["town"]}, {vacancy["salary"]}, '
                          f'{vacancy["currency"]}, {vacancy["description"]}, {vacancy["link"]}')
                print('-' * 108)
        except IndexError('Список с вакансиями пуст.'):
            pass

    @staticmethod
    def print_options(data_collection):
        """
        Метод выводит в консоль параметры поискового запроса.
        :param data_collection: словарь с поисковыми ключами пользователя: dict
        :return: None
        """
        print('Параметры поиска, которые вы выбрали:')
        print(f'1. Поисковой запрос: {data_collection["search_query"]}')
        print(f'2. Колличество вакансий для топа: {data_collection["top_n"]}')
        print(f'3. Платформа для поиска: {data_collection["platform_name"]}')
        print(f'4. Фильтр по ключевым словам: {data_collection["is_filter"]}')
        if data_collection['is_filter']:
            print(f'4.1 Слова для фильтра: {", ".join(data_collection["filter_words"])}')
        print(f'5. Сортировка по зарплате: {data_collection["is_sort"]}')
        if data_collection['is_sort']:
            print(f'5.1 Порядок сортировки: {data_collection["text_reverse"]}')

    @staticmethod
    def print_for_del(top_vacancy, vacancy_options_cls, vacancy_cls):
        """
        Метод для отображения текущего топ списка вакансий, удаление ненужных вакансий
        :param top_vacancy: список экземпляров класса Vacancy: list
        :param vacancy_options_cls: Класс для работы с вакансиями: class
        :param vacancy_cls: Класс для сохранения вакансий в файл и последующей работы с ним: class
        :return: None
        """
        while True:
            if len(top_vacancy) == 0:
                print('>> Вы слишком увлеклись и теперь список с вакансиями пуст.'
                      '\n>> Работа с удалением завершается аварийно.')
                break
            print('-' * 108)
            for num, vacancy in enumerate(top_vacancy, start=1):
                print(f'{num} - {vacancy}')
            print('-' * 108)
            print('Чтобы закончить работу со списком вакансий введите "стоп" или "stop."')
            enter_data = input('Введите номер удаляемой вакансии: ')
            if enter_data == 'stop' or enter_data == 'стоп':
                break
            else:
                if enter_data.isalpha() or enter_data == '':
                    print('>> Так не пойдет.. нужно ввести цифру.')
                    continue
            vacancy_options_cls.del_vacancy(vacancy_cls.all, top_vacancy, enter_data)

    @staticmethod
    def print_if_vacancy_list_empty(user_interaction):
        """
        Метод сообщает, что текущий список вакансий пуст.
        Предлагает начать поиск сначала.
        :param user_interaction: основная функция, которая запускает весь код программы: function
        :return: None
        """
        print('>> Что-то пошло не так и список с вакансиями пуст.')
        while True:
            print('Чтобы начать сначала введите "старт" или "start."'
                  '\nЧтобы закончить работу введите "стоп" или "stop."')
            user_enter = input()
            if user_enter == 'старт' or user_enter == 'start':
                user_interaction()
            elif user_enter == 'стоп' or user_enter == 'stop':
                break
