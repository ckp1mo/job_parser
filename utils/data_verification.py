class DataVerification:
    """
    Класс для получения и обработки параметров поиска.
    """
    @staticmethod
    def get_search_query():
        """
        Запрос на ключ для поиска вакансий
        :return: строковое значение -> str
        """
        search_query = input('Введите поисковый запрос: ')
        if len(search_query) == 0:
            search_query = 'python'
        return search_query

    @staticmethod
    def get_top_n():
        """
        Метод для получения колличества вывода вакансий
        :return: чиловое значение -> int
        """
        top_n = input('Введите количество вакансий для вывода в топ: ')
        if len(top_n) > 0:
            for i in top_n:
                if i.isalpha():
                    top_n = 20
                    break
        else:
            top_n = 20
        print('-' * 108)
        top_n = int(top_n)
        return top_n

    @staticmethod
    def get_platform():
        """
        Метод для получения платформы для поиска вакансий, а так же имени ее
        :return: строковое значение -> str
        """
        platforms = input('Выберите платформы для поиска: '
                          '\n1. HeadHunter'
                          '\n2. SuperJob'
                          '\n3. Обе платформы\n')
        if len(platforms) > 0:
            if platforms == '1':
                platforms = platforms
                platform_name = 'HeadHunter'
            elif platforms == '2':
                platforms = platforms
                platform_name = 'SuperJob'
            elif platforms == '3':
                platforms = platforms
                platform_name = 'HeadHunter и SuperJob'
            else:
                platforms = '3'
                platform_name = 'HeadHunter и SuperJob'
        else:
            platforms = '3'
            platform_name = 'HeadHunter и SuperJob.'
        return platforms, platform_name

    @staticmethod
    def get_is_filter():
        """
        Метод для уточнения фильтрации вакансий по словам
        :return: строковое значение -> str
        """
        is_filter = False
        filter_words = []
        print('Хотели бы Вы отфильтровать вакансии по ключевым словам?: '
              '\n1. Да'
              '\n2. Нет')
        filter_data = input()
        if filter_data == '1':
            is_filter = True
            filter_words = input("Введите ключевые слова для фильтрации вакансий: ").lower().split()
            if len(filter_words) == 0:
                is_filter = False
        elif filter_data == '2':
            is_filter = False
        return is_filter, filter_words

    @staticmethod
    def get_is_sort():
        """
        Метод для уточнения сортировки вакансий по зарплате
        :return: строковое значение -> str
        """
        is_sort = False
        is_reverse = False
        text_reverse = ''
        print('Хотели бы вы отсортировать вакансии по зарплате?'
              '\n1. Да'
              '\n2. Нет')
        sort_data = input()
        if sort_data == '1':
            is_sort = True
            print('Какой тип сортировки использовать?'
                  '\n1. По возрастанию'
                  '\n2. По убыванию')
            reverse_data = input()
            if reverse_data == '2':
                is_reverse = True
                text_reverse = 'По убыванию'
            elif reverse_data == '1':
                is_reverse = False
                text_reverse = 'По возрастанию'
            else:
                is_sort = False
                text_reverse = 'Отсутствует'
        elif sort_data == '2':
            is_sort = False
        return is_sort, is_reverse, text_reverse

    @staticmethod
    def get_data_for_del():
        """
        Метод для уточнения об удалении вакансий
        :return: булевое знчение ->
        """
        is_del = False
        print('Хотели бы вы удалить некоторые вакансии перед сохранением их в файл?'
              '\n1. Да'
              '\n2. Нет')
        if input() == '1':
            is_del = True
        return is_del
