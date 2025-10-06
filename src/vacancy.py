from __future__ import annotations
from typing import Dict, Any, Optional


class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = ('_title', '_url', '_salary_from', '_salary_to', '_currency',
                 '_description', '_requirements', '_employer')

    def __init__(self, title: str, url: str, salary_from: Optional[int] = None,
                 salary_to: Optional[int] = None, currency: str = "",
                 description: str = "", requirements: str = "", employer: str = ""):
        self._title = self._validate_title(title)
        self._url = self._validate_url(url)
        self._salary_from = self._validate_salary(salary_from)
        self._salary_to = self._validate_salary(salary_to)
        self._currency = currency
        self._description = description
        self._requirements = requirements
        self._employer = employer

    def _validate_title(self, title: str) -> str:
        """Валидация названия вакансии"""
        if not title or not isinstance(title, str):
            raise ValueError("Название вакансии должно быть непустой строкой")
        return title.strip()

    def _validate_url(self, url: str) -> str:
        """Валидация URL вакансии"""
        if not url.startswith(('http://', 'https://')):
            raise ValueError("URL вакансии должен начинаться с http:// или https://")
        return url

    def _validate_salary(self, salary: Optional[int]) -> int:
        """Валидация зарплаты"""
        if salary is None:
            return 0
        if not isinstance(salary, (int, float)) or salary < 0:
            return 0
        return int(salary)

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary_from(self) -> int:
        return self._salary_from

    @property
    def salary_to(self) -> int:
        return self._salary_to

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def description(self) -> str:
        return self._description

    @property
    def requirements(self) -> str:
        return self._requirements

    @property
    def employer(self) -> str:
        return self._employer

    def get_avg_salary(self) -> float:
        """Получение средней зарплаты"""
        if self._salary_from and self._salary_to:
            return (self._salary_from + self._salary_to) / 2
        elif self._salary_from:
            return self._salary_from
        elif self._salary_to:
            return self._salary_to
        return 0.0

    # Методы сравнения по зарплате
    def __eq__(self, other: Vacancy) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_avg_salary() == other.get_avg_salary()

    def __lt__(self, other: Vacancy) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_avg_salary() < other.get_avg_salary()

    def __le__(self, other: Vacancy) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_avg_salary() <= other.get_avg_salary()

    def __gt__(self, other: Vacancy) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_avg_salary() > other.get_avg_salary()

    def __ge__(self, other: Vacancy) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_avg_salary() >= other.get_avg_salary()

    def __str__(self) -> str:
        salary_info = "Зарплата не указана"
        if self._salary_from or self._salary_to:
            salary_parts = []
            if self._salary_from:
                salary_parts.append(f"от {self._salary_from}")
            if self._salary_to:
                salary_parts.append(f"до {self._salary_to}")
            salary_info = f"{' '.join(salary_parts)} {self._currency}"

        return (f"Вакансия: {self._title}\n"
                f"Компания: {self._employer}\n"
                f"Зарплата: {salary_info}\n"
                f"Ссылка: {self._url}\n")

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование вакансии в словарь"""
        return {
            'title': self._title,
            'url': self._url,
            'salary_from': self._salary_from,
            'salary_to': self._salary_to,
            'currency': self._currency,
            'description': self._description,
            'requirements': self._requirements,
            'employer': self._employer
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Vacancy:
        """Создание вакансии из словаря"""
        return cls(
            title=data.get('title', ''),
            url=data.get('url', ''),
            salary_from=data.get('salary_from'),
            salary_to=data.get('salary_to'),
            currency=data.get('currency', ''),
            description=data.get('description', ''),
            requirements=data.get('requirements', ''),
            employer=data.get('employer', '')
        )

    @staticmethod
    def cast_to_object_list(vacancies_data: list[Dict[str, Any]]) -> list[Vacancy]:
        """Преобразование списка словарей в список объектов Vacancy"""
        vacancies = []
        for vacancy_data in vacancies_data:
            try:
                # Парсинг данных из API HH.ru
                salary_data = vacancy_data.get('salary')
                salary_from = salary_data.get('from') if salary_data else None
                salary_to = salary_data.get('to') if salary_data else None
                currency = salary_data.get('currency', '') if salary_data else ''

                vacancy = Vacancy(
                    title=vacancy_data.get('name', ''),
                    url=vacancy_data.get('alternate_url', ''),
                    salary_from=salary_from,
                    salary_to=salary_to,
                    currency=currency,
                    description=vacancy_data.get('snippet', {}).get('responsibility', ''),
                    requirements=vacancy_data.get('snippet', {}).get('requirement', ''),
                    employer=vacancy_data.get('employer', {}).get('name', '')
                )
                vacancies.append(vacancy)
            except (ValueError, KeyError) as e:
                print(f"Ошибка при создании вакансии: {e}")
                continue

        return vacancies