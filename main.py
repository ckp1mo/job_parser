from src.user_interaction import user_interaction, get_started
from src.vacancy import VacancyOptions, JSONSaver, Vacancy
from pathlib import Path
from utils.print_info import PrintInfo

OUTPUT_FILES = Path(Path.cwd(), 'output_files')


print('Привет!')
# Создаем списочек с файлами из директории 'output_files'
file_list = [files.name for files in OUTPUT_FILES.glob('*.json') if files.exists()]
# Если списочек с файлами пуст, начинает новый поиск
if len(file_list) > 0:
    # Вызов функции get_started, потому что у нас есть файлы, в которых множно что-то поискать
    file_name = get_started(file_list)
    file_path = Path(Path.cwd(), 'output_files', f'{file_name}')
    # Если функция что-то вернула, значит идем искать по ключевым словам
    if file_name:
        while True:
            key_word = input('Введите ключевые слова для поиска по вакансиям: ').lower().split()
            # Вызывается метод get_by_key() класса VacancyOptions, для создания списка с вакансиями по ключевым словам
            vacancy_list_by_key = VacancyOptions().get_by_key(file_path, key_word)
            if vacancy_list_by_key is None or len(vacancy_list_by_key) == 0:
                print('>> Поиск по ключевым словам не удался\n')
                user_repeat = input('Попробуем снова или начать новый поиск вакансий?'
                                    '\n1. Попробовать еще раз'
                                    '\n2. Начать новый поиск\n')
                if user_repeat == '1':
                    continue
                elif user_repeat == '2':
                    print('>> Понял, принял. Исполняю')
                    user_interaction()
                else:
                    print('>> Это не то, что я ожидаю.. начнем новый поиск тогда')
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
                # Запускаем классметод создания вакансий из JSON файла
                Vacancy.vacancy_to_instance(vacancy_list_by_key)
                # Получаем в переменную имя нового файла
                file_name = JSONSaver().get_file_name()
                # Сохранение отобранных вакансий в файл
                JSONSaver().save_vacancy(Vacancy.all, file_name)
                print(f'>> Вакансии сохранены, ищи их в рабочей директори по пути /output_files/{file_name}.json')
                print('>> Хорошего дня! :)')
                break
            elif user_repeat == '2':
                continue
            elif user_repeat == '3':
                user_interaction()
            else:
                print('>> Хорошего дня! :)')
                break
    else:
        user_interaction()
else:
    print('Первый раз значит..')
    user_interaction()
