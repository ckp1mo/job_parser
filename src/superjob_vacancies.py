from src.vacancies import Vacancies
import requests
import os
from pathlib import Path
import json


class SuperJobApi(Vacancies):

    def __init__(self, vacancy, town, payment_from, payment_to):
        self.vacancy = vacancy
        self.town = town
        self.payment_from = payment_from
        self.payment_to = payment_to

    def get_vacancies(self):
        # получение вакансий с суперджоб
        params = {
            'keyword': self.vacancy,
            'town': self.town,
            'payment_from': self.payment_from,
            'payment_to': self.payment_to,
            'page': 0,
            'count': 3
        }
        url = 'https://api.superjob.ru/2.0/vacancies/'
        # token_response = requests.get('https://api.superjob.ru/2.0/oauth2/password/?login=nekonea@gmail.com&password=dbreyz12&client_id=3088&client_secret=v3.r.137885645.94fe61335eadd06fa24986573c2aa77bc7b3f67e.2855bed0c127c683832fc7b80de1b13fd05c4606')
        # token = token_response.json()
        response = requests.get(url, headers={"X-Api-App-Id": os.getenv('SuperJobKey'), 'Authorization': 'Bearer v3.r.137885645.79ed4b9fe67e570ab857454386fed559827513d4.2f0acf2f14b5a89f5de31f455541a2b370cd6465'},
                                params=params)

        # output_vacancies = Path.cwd() / 'superjob_vacancies.json'
        # output_vacancies.write_text(json.dumps(response.json(), ensure_ascii=False, indent=4), encoding='utf-8')
        with open('superjob_vacancies.json', 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)


r = SuperJobApi('python', 'Moscow', 50000, 15000)
r.get_vacancies()
