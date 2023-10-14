import json
from pathlib import Path

file = Path.cwd()/'superjob_vacancies.json'
# print(Path.cwd()/'superjob_vacancies.json')


class VacanciesOptions:

    def __init__(self, vacancies_json):
        self.vacancies_json = vacancies_json
        # self.name = name
        # self.url = url
        # self.salary = salary
        # self.description = description
        with open(self.vacancies_json, 'r', encoding='utf-8', errors='ignore') as f:
            print(json.load(f))


a = VacanciesOptions(file)
