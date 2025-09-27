from abc import ABC, abstractmethod
from typing import Any

class BaseAPI(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями"""

    @abstractmethod
    def __init__(self, base_url: str):
        self._base_url = base_url

    @abstractmethod
    def _connect(self) -> bool:
        """Проверка подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str, per_page: int = 100) -> list[dict[str, Any]]:
        """Получение вакансий по поисковому запросу"""
        pass