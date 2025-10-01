from abc import ABC, abstractmethod
from src.vacancy import Vacancy
from typing import Any


class BaseStorage(ABC):
    """Абстрактный класс для работы с хранилищем вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        """Добавление вакансии в хранилище"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: dict[str, Any] = None) -> list[Vacancy]:
        """Получение вакансий по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из хранилища"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Очистка хранилища"""
        pass