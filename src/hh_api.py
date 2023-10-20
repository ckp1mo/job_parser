import requests
from src.abstract_class import RequestApi, ConvertProcessor

URL = 'https://api.hh.ru/vacancies'


class HHRequestApi(RequestApi):
    """
    Класс для работы с платформой HeadHunter через API запрос
    """
    def __init__(self, text='python'):
        self.__url = URL
        self.text = text

    def get_vacancies(self):
        """
        Делает запрос по API
        :return: возвращает ответ формат -> json
        """
        params = {
            'text': self.text,
            'page': 0,
            'per_page': 50,
            'only_with_salary': 'true',
            'area': '113'
        }
        response_hh = requests.get(self.__url, headers={'User-Agent': 'slon'},
                                   params=params)
        return response_hh.json()


class HHVacancy(ConvertProcessor):
    """
    Класс для отбора нужный ключей, значений и параметров вакансии.
    """
    vacancy_list = []

    def __init__(self, response):
        self.response = response

    def vacancy_to_list(self):
        """
        Метод vacancy_to_list вычленяет из массива заданные значения.
        :return: Возвращает список словарей с заданными ключами и значениями -> list
        """
        for vacancy in self.response['items']:
            description = vacancy['snippet']['requirement']
            if description is None:
                description = 'Нет описания'
            else:
                description = description.replace('<highlighttext>', '')
                description = description.replace('</highlighttext>', '')
            if vacancy['salary']['from'] is None:
                salary = vacancy['salary']['to']
            else:
                salary = vacancy['salary']['from']

            HHVacancy.vacancy_list.append(
                {'vacancy': vacancy['name'],
                 'town': vacancy['area']['name'],
                 'salary': salary,
                 'currency': vacancy['salary']['currency'],
                 'description': description[0:150],
                 'link': vacancy['alternate_url']
                 }
            )
        return HHVacancy.vacancy_list
