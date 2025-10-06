from src.vacancy import Vacancy
import os

def create_test_vacancy(title="Test Vacancy", employer="Test Company"):
    """Создание тестовой вакансии"""
    return Vacancy(
        title=title,
        url=f"https://hh.ru/vacancy/{title.replace(' ', '_')}",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
        description="Test description",
        requirements="Test requirements",
        employer=employer
    )

def cleanup_file(filename):
    if os.path.exists(filename):
        os.remove(filename)