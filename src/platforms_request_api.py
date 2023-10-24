from src.abstract_class import RequestApi
import requests
import os


URL_SJ = 'https://api.superjob.ru/2.0/vacancies/'
URL_HH = 'https://api.hh.ru/vacancies'
LOGIN = os.getenv('SJLogin')
PASSWORD = os.getenv('SJPassword')
CLIENT_ID = os.getenv('SJClientID')
SECRET_KEY = os.getenv('SJSecretKey')


class PlatformsRequestApi(RequestApi):
    """
    Класс для работы с платформами через API запрос
    """

    def __init__(self, text='python'):
        self.__url_sj = URL_SJ
        self.__url_hh = URL_HH
        self.text = text

    def get_vacancies_sj(self):
        """
        Делает запрос по API
        :return: возвращает ответ формат -> json
        """
        params = {
            'keyword': self.text,
            'page': 0,
            'count': 50,
        }
        token_response = requests.get(f'https://api.superjob.ru/2.0/oauth2/password/?login={LOGIN}&password={PASSWORD}'
                                      f'&client_id={CLIENT_ID}&client_secret={SECRET_KEY}')
        token = token_response.json()
        response = requests.get(self.__url_sj, headers={"X-Api-App-Id": SECRET_KEY,
                                                        'Authorization': f'{token["token_type"]} '
                                                                         f'{token["access_token"]}'},
                                params=params)
        return response.json()

    def get_vacancies_hh(self):
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
        response = requests.get(self.__url_hh, headers={'User-Agent': 'slon'},
                                params=params)
        return response.json()
