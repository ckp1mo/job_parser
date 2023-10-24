from src.abstract_class import VacancyMethod, VacancySaver
from pathlib import Path
import json


# директория для сохранения пользовательских файлов
OUTPUT_DIR = Path(Path.cwd(), 'output_files')


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

    @classmethod
    def vacancy_to_list_hh(cls, response):
        """
        Метод создает экземпляры класса из ответа по API запросу от сервера HeadHunter,
        предворительно выбирая нужные ключи из массива.
        """
        vacancy_list = []
        for vacancy in response['items']:
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

            vacancy_list.append(
                {'vacancy': vacancy['name'],
                 'town': vacancy['area']['name'],
                 'salary': salary,
                 'currency': vacancy['salary']['currency'],
                 'description': description[0:150],
                 'link': vacancy['alternate_url']
                 }
            )
        for key in vacancy_list:
            cls(key['vacancy'], key['town'], key['salary'], key['currency'], key['description'], key['link'])

    @classmethod
    def vacancy_to_list_sj(cls, response):
        """
        Метод создает экземпляры класса из ответа по API запросу от сервера SuperJob,
        предворительно выбирая нужные ключи из массива.
        """
        vacancy_list = []
        for vacancy in response['objects']:
            description = vacancy['candidat']
            if vacancy['payment_from'] is None:
                salary = vacancy['payment_to']
            else:
                salary = vacancy['payment_from']

            vacancy_list.append(
                {'vacancy': vacancy['profession'],
                 'town': vacancy['town']['title'],
                 'salary': salary,
                 'currency': vacancy['currency'],
                 'description': description[0:150],
                 'link': vacancy['link']
                 }
            )
        for key in vacancy_list:
            cls(key['vacancy'], key['town'], key['salary'], key['currency'], key['description'], key['link'])


class JSONSaver(VacancySaver):
    """
    Класс для сохранения вакансий в файл.
    """
    def save_vacancy(self, array):
        """
        Метод формирует словарь с ключами по атрибутам класса Vacancy и далее сохраняет его
        в формате json в файл в рабочей директории по пути 'output_files/*.json'
        :return: None
        """
        to_json = []
        if not OUTPUT_DIR.exists():
            OUTPUT_DIR.mkdir()
        file_name = input('Введите имя файля для сохранения: \n')
        if len(file_name) == 0:
            file_name = 'nameless'
        vacancy_file = Path(Path.cwd(), 'output_files', f'{file_name}.json')
        vacancy_file.touch()
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
            print('>> Файл не найден')
        except json.JSONDecodeError:
            print('>> Файл испорчен')
        except TypeError:
            print('>> Неккоректный формат вакансий')
        except KeyError:
            print('>> Неккоректный формат вакансий')

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
