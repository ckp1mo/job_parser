from src.abstract_class import VacancyMethod, VacancySaver
from pathlib import Path
import json


# OUTPUT_DIR - директория для сохранения файла VACANCY_FILE
OUTPUT_DIR = Path(Path.cwd(), 'output_files')
VACANCY_FILE = Path(Path.cwd(), 'output_files', 'vacancy.json')
VACANCY_FILE_FILTERED = Path(Path.cwd(), 'output_files', 'vacancy_filtered.json')


class Vacancy:
    """
    Класс для создания вакансий в унифицированном формате.
    """
    all = []

    def __init__(self, vacancy, town, salary, currency, description, link):
        self.vacancy = vacancy
        self.town = town
        self.salary = salary
        self.currency = currency
        self.description = description
        self.link = link
        Vacancy.all.append(self)

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.vacancy}", "{self.town}", "{self.salary}", "{self.currency}", ' \
               f'"{self.description}", "{self.description}")'

    def __str__(self):
        self.description = self.description.replace('\n', ' ')
        return f'{self.vacancy}, {self.town}, {self.salary}, {self.currency}, {self.description}, {self.link}'

    def __gt__(self, other):
        return int(self.salary) > int(other.salary)

    def __lt__(self, other):
        return int(self.salary) < int(other.salary)

    @classmethod
    def vacancy_to_instance(cls, array):
        """
        Метод для создания экземпляров класса из словаря по ключам
        :param array: словарь с ключами 'vacancy', 'town', 'salary', 'currency'', 'description', 'link'
        :return: None
        """
        for key in array:
            cls(key['vacancy'], key['town'], key['salary'], key['currency'], key['description'], key['link'])


class JSONSaver(VacancySaver):
    """
    Класс для сохранения вакансий в файл.
    """
    def save_vacancy(self, array):
        """
        Метод формирует словарь с ключами по атрибутам класса Vacancy и далее
        сохраняет его в формате json в файл в рабочей директории по пути 'output_files/vacancy.json'
        При повторном фильтре из файла путь будет 'output_files/vacancy_filtered.json'
        :return: None
        """
        to_json = []
        if not OUTPUT_DIR.exists():
            OUTPUT_DIR.mkdir()
        if VACANCY_FILE.exists():
            vacancy_file = VACANCY_FILE_FILTERED
        else:
            vacancy_file = VACANCY_FILE

        with open(vacancy_file, 'w', encoding='utf-8') as f:
            for x in array:
                to_json.append({
                    'vacancy': x.vacancy,
                    'town': x.town,
                    'salary': x.salary,
                    'currency': x.currency,
                    'description': x.description,
                    'link': x.link
                })
            json.dump(to_json, f, ensure_ascii=False, indent=4)


class VacancyOptions(VacancyMethod):
    """
    Класс для работы с экземплярами класса Vacancy.
    """
    def get_by_key(self, output_file, key_word):
        """
        Метод достает из раннее сохраненного файла вакансии по заданным ключам.
        :return: экземпляры класса -> list
        """
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                vacancy_list = []
                data = json.load(f)
                for num, copy in enumerate(data, start=1):
                    for word in key_word:
                        if word in copy['vacancy'].lower() or word in copy['description'].lower():
                            vacancy_list.append(copy)
                            break
                return vacancy_list
        except FileNotFoundError:
            print('Файл не найден')

    def del_vacancy(self, top_vacancy, enter_data):
        """
        Метод удаляет выбранную вакансию.
        :return: None
        """
        try:
            if int(enter_data) != 0:
                del top_vacancy[int(enter_data) - 1]
            else:
                print('Промазал.. нет такой строчки.\n')
        except IndexError:
            print('Промазал.. нет такой строчки.\n')