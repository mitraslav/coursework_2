from src.hh_api import HeadHunterAPI
from src.vacancy import Vacancy
from src.json_storage import JSONStorage
from src.utils import (filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, print_vacancies)

def user_interaction():
    """Функция для взаимодействия с пользователем"""
    print("Добро пожаловать в программу для поиска вакансий!")
    print("=" * 50)

    hh_api = HeadHunterAPI()
    storage = JSONStorage()

    search_query = input("Введите поисковый запрос (например: Python разработчик): ").strip()

    try:
        per_page = int(input("Введите количество вакансий для загрузки (по умолчанию 100): ") or "100")
    except ValueError:
        per_page = 100

    try:
        top_n = int(input("Введите количество вакансий для вывода в топ N: ").strip())
    except ValueError:
        top_n = 10

    filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").strip().split()
    salary_range = input("Введите диапазон зарплат (например: 100000-150000): ").strip()

    print("\nЗагружаю вакансии...")

    try:
        hh_vacancies_data = hh_api.get_vacancies(search_query, per_page)
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies_data)

        for vacancy in vacancies_list:
            storage.add_vacancy(vacancy)

        print(f"Загружено {len(vacancies_list)} вакансий")

        filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
        ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
        sorted_vacancies = sort_vacancies(ranged_vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

        print(f"\nНайдено {len(top_vacancies)} вакансий из запрошенных {top_n}:")
        print_vacancies(top_vacancies)

        while True:
            print("\nДополнительные возможности:")
            print("1. Поиск по сохраненным вакансиям")
            print("2. Очистить базу вакансий")
            print("3. Выйти")

            choice = input("Выберите действие (1-3): ").strip()

            if choice == '1':
                search_criteria = input("Введите ключевое слово для поиска в сохраненных вакансиях: ").strip()
                if search_criteria:
                    criteria = {'title': search_criteria.lower()}
                    found_vacancies = storage.get_vacancies(criteria)
                    print(f"\nНайдено {len(found_vacancies)} вакансий:")
                    print_vacancies(found_vacancies)

                elif choice == '2':
                    confirm = input("Вы уверены, что хотите очистить базу вакансий? (да/нет): ").strip().lower()
                    if confirm == 'да':
                        storage.clear()
                        print("База вакансий очищена.")

                elif choice == '3':
                    print("До свидания!")
                    break

                else:
                    print("Неверный выбор. Попробуйте снова.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == '__main__':
    user_interaction()

