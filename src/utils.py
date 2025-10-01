from src.vacancy import Vacancy

def filter_vacancies(vacancies: list[Vacancy], filter_words: list[str]) -> list[Vacancy]:
    """Фильтрация вакансий по ключевым словам"""
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        vacancy_text = f"{vacancy.title} {vacancy.description} {vacancy.requirements}".lower()
        if any(word.lower() in vacancy_text for word in filter_words):
            filtered.append(vacancy)

    return filtered

def get_vacancies_by_salary(vacancies: list[Vacancy], salary_range: str) -> list[Vacancy]:
    """Фильтрация вакансий по диапазону зарплат"""
    if not salary_range:
        return vacancies

    try:
        if '-' in salary_range:
            salary_from, salary_to = map(int, salary_range.split('-'))
        else:
            salary_from = int(salary_range)
            salary_to = float('inf')
    except ValueError:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        avg_salary = vacancy.get_avg_salary()
        if salary_from <= avg_salary <= salary_to:
            filtered.append(vacancy)

    return filtered

def sort_vacancies(vacancies: list[Vacancy]) -> list[Vacancy]:
    """Сортировка вакансий по убыванию зарплаты"""
    return sorted(vacancies, reverse=True)

def get_top_vacancies(vacancies: list[Vacancy], top_n: int) -> list[Vacancy]:
    """Получение топ N вакансий"""
    return vacancies[:top_n]

def print_vacancies(vacancies: list[Vacancy]) -> None:
    """Вывод вакансий в читаемом формате"""
    if not vacancies:
        print('Вакансии не найдены."')
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{'='*50}")
        print(f"вакансия #{i}")
        print(f"{'=' * 50}")
        print(vacancy)