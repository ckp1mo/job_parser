from src.abstract_class import RequestApi, ConvertProcessor
import requests
import os


URL = 'https://api.superjob.ru/2.0/vacancies/'
LOGIN = os.getenv('SJLogin')
PASSWORD = os.getenv('SJPassword')
CLIENT_ID = os.getenv('SJClientID')
SECRET_KEY = os.getenv('SJSecretKey')


class SJRequestApi(RequestApi):
    """
    Класс для работы с платформой SuperJob через API запрос
    """
    def __init__(self, keyword='python'):
        self.__url = URL
        self.keyword = keyword

    def get_vacancies(self):
        """
        Делает запрос по API
        :return: возвращает ответ формат -> json
        """
        params = {
            'keyword': self.keyword,
            'page': 0,
            'count': 50,
        }
        token_response = requests.get(f'https://api.superjob.ru/2.0/oauth2/password/?login={LOGIN}&password={PASSWORD}'
                                      f'&client_id={CLIENT_ID}&client_secret={SECRET_KEY}')
        token = token_response.json()
        response = requests.get(self.__url, headers={"X-Api-App-Id": SECRET_KEY,
                                                     'Authorization': f'{token["token_type"]} {token["access_token"]}'},
                                params=params)
        return response.json()


class SJVacancy(ConvertProcessor):
    """
    Класс для отбора нужный ключей и значений и параметров вакансии.
    """
    vacancy_list = []

    def __init__(self, response):
        self.response = response

    def vacancy_to_list(self):
        """
        Метод vacancy_to_list вычленяет из массива заданные значения.
        :return: Возвращает список словарей с заданными ключами и значениями -> list
        """
        for vacancy in self.response['objects']:
            description = vacancy['candidat']
            if vacancy['payment_from'] is None:
                salary = vacancy['payment_to']
            else:
                salary = vacancy['payment_from']

            SJVacancy.vacancy_list.append(
                {'vacancy': vacancy['profession'],
                 'town': vacancy['town']['title'],
                 'salary': salary,
                 'currency': vacancy['currency'],
                 'description': description[0:150],
                 'link': vacancy['link']
                 }
            )
        return SJVacancy.vacancy_list
