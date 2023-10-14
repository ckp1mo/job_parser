from abc import abstractmethod, ABC


class Vacancies(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass
