from abc import abstractmethod, ABC


class RequestApi(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass


class ConvertProcessor(ABC):

    @abstractmethod
    def vacancy_to_list(self):
        pass


class VacancyMethod(ABC):

    @abstractmethod
    def get_by_key(self, output_file, key_word):
        pass

    @abstractmethod
    def del_vacancy(self, vacancy_list, enter_data):
        pass


class VacancySaver(ABC):

    @abstractmethod
    def save_vacancy(self, array):
        pass
