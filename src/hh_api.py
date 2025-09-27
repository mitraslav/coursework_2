import requests
from typing import Any
from src.base_api import BaseAPI

class HeadHunterAPI(BaseAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self._base_url = "https://api.hh.ru/vacancies"
        self._headers = {'User-Agent': 'HH-User-Agent'}

    def _connect(self) -> bool:
        """Проверка подключения к API HH"""

        try:
            response = requests.get(self._base_url, headers=self._headers, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_vacancies(self, search_query: str, per_page: int = 100) -> list[dict[str, Any]]:
        """Получение вакансий с hh.ru по поисковому запросу"""
        if not self._connect():
            raise ConnectionError("Не удалось подключиться к API HH.ru")

        params = {
            'text': search_query,
            'area': 113,
            'per_page': per_page,
            'page': 0
        }

        try:
            response = requests.get(self._base_url, params=params, headers=self._headers)
            response.raise_for_status()
            data = response.json()
            return data.get('items', [])
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка при запросе к API: {e}")