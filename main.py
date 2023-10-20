from src.user_interaction import user_interaction, get_started
from src.vacancy import VacancyOptions, JSONSaver, Vacancy
from pathlib import Path
from utils.print_info import PrintInfo

VACANCY_FILE = Path(Path.cwd(), 'output_files', 'vacancy.json')
VACANCY_FILE_FILTERED = Path(Path.cwd(), 'output_files', 'vacancy_filtered.json')


print('Привет!')
if VACANCY_FILE.exists():
    bool_ = get_started()
    if bool_:
        while True:
            key_word = input('Введите ключевые слова для поиска по вакансиям: ').lower().split()
            vacancy_list_by_key = VacancyOptions().get_by_key(VACANCY_FILE, key_word)
            if len(vacancy_list_by_key) == 0:
                print('Поиск по ключевым словам не удался')
                user_repeat = input('Попробуем снова или начать новый поиск вакансий?'
                                    '\n1. Попробовать еще раз'
                                    '\n2. Начать новый поиск\n')
                if user_repeat == '1':
                    continue
                elif user_repeat == '2':
                    print('Понял, принял. Исполняю')
                    user_interaction()
                else:
                    print('Это не то, что я ожидаю.. начнем новый поиск тогда')
                    user_interaction()
            try:
                PrintInfo().print_vacancy(vacancy_list_by_key)
            except IndexError:
                print('Что-то случилось.. ')
            user_repeat = input('Попробуем снова или начать новый поиск вакансий?'
                                '\n1. Сохранить результаты в новый файл'
                                '\n2. Попробовать еще раз'
                                '\n3. Начать новый поиск'
                                '\n4. Завершить программу\n')
            if user_repeat == '1':
                if VACANCY_FILE_FILTERED.exists():
                    VACANCY_FILE_FILTERED.unlink()
                Vacancy.vacancy_to_instance(vacancy_list_by_key)
                JSONSaver().save_vacancy(Vacancy.all)
                print('Вакансии сохранены, ищи их в рабочей директори по пути /output_files/vacancy_filtered.json')
                print('Хорошего дня! :)')
                break
            elif user_repeat == '2':
                continue
            elif user_repeat == '3':
                user_interaction()
            else:
                print('Хорошего дня! :)')
                break
    else:
        user_interaction()
else:
    print('Первый раз значит..')
    user_interaction()
