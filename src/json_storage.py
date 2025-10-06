import json
import os
from typing import Any
from src.vacancy import Vacancy
from src.base_storage import BaseStorage

class JSONStorage(BaseStorage):
    """Класс для работы с JSON-файлом как хранилищем вакансий"""

    def __init__(self, filename: str = 'vacancies.json'):
        self._filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создание файла, если он не существует"""
        if not os.path.exists(self._filename):
            with open(self._filename, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _read_vacancies(self) -> list[dict[str, Any]]:
        """Чтение вакансий из файла"""
        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_vacancies(self, vacancies_data: list[dict[str, Any]]) -> None:
        """Запись вакансий в файл"""
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies_data, f, ensure_ascii=False, indent=2)

    def _vacancy_exists(self, vacancy: Vacancy, vacancies_data: list[dict[str, Any]]) -> bool:
        """Проверка существования вакансии"""
        vacancy_dict = vacancy.to_dict()
        for existing_vacancy in vacancies_data:
            if (existing_vacancy['title'] == vacancy_dict['title'] and
                    existing_vacancy['employer'] == vacancy_dict['employer'] and
                    existing_vacancy['url'] == vacancy_dict['url']):
                return True
        return False  # ← ИСПРАВЛЕНИЕ: возвращаем False после проверки ВСЕХ вакансий

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в JSON-файл"""
        vacancies_data = self._read_vacancies()
        vacancy_dict = vacancy.to_dict()

        if not self._vacancy_exists(vacancy, vacancies_data):
            vacancies_data.append(vacancy_dict)
            self._write_vacancies(vacancies_data)

    def get_vacancies(self, criteria: dict[str, Any] = None) -> list[Vacancy]:
        """Получение вакансий по критериям"""
        vacancies_data = self._read_vacancies()
        vacancies = [Vacancy.from_dict(data) for data in vacancies_data]

        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            matches = True
            for key, value in criteria.items():
                if hasattr(vacancy, key):
                    attr_value = getattr(vacancy, key)
                    if value not in str(attr_value).lower():
                        matches = False
                        break
                else:
                    matches = False
                    break

            if matches:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из JSON-файла"""
        vacancies_data = self._read_vacancies()
        vacancy_dict = vacancy.to_dict()

        vacancies_data = [v for v in vacancies_data
                          if not (v['title'] == vacancy_dict['title'] and
                                  v['employer'] == vacancy_dict['employer'] and
                                  v['url'] == vacancy_dict['url'])]
        self._write_vacancies(vacancies_data)

    def clear(self) -> None:
        """Очистка JSON-файла"""
        self._write_vacancies([])