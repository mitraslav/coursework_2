from src.vacancy import Vacancy


def test_vacancy_creation():
    """Тест создания вакансии"""
    print("🧪 Тест создания вакансии...")

    vacancy = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
        description="Разработка backend на Python",
        requirements="Опыт работы 3+ года, Django, Flask",
        employer="Tech Company"
    )

    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.currency == "RUR"
    assert vacancy.description == "Разработка backend на Python"
    assert vacancy.requirements == "Опыт работы 3+ года, Django, Flask"
    assert vacancy.employer == "Tech Company"

    print("✓ Создание вакансии работает")


def test_vacancy_creation_minimal():
    """Тест создания вакансии с минимальными данными"""
    print("🧪 Тест создания вакансии с минимальными данными...")

    vacancy = Vacancy(
        title="Java Developer",
        url="https://hh.ru/vacancy/456"
    )

    assert vacancy.title == "Java Developer"
    assert vacancy.url == "https://hh.ru/vacancy/456"
    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0
    assert vacancy.currency == ""
    assert vacancy.description == ""
    assert vacancy.requirements == ""
    assert vacancy.employer == ""

    print("✓ Создание вакансии с минимальными данными работает")


def test_vacancy_validation():
    """Тест валидации данных"""
    print("🧪 Тест валидации данных...")

    # Тест пустого названия
    try:
        Vacancy(title="", url="https://hh.ru/vacancy/123")
        assert False, "Ожидалась ошибка валидации"
    except ValueError as e:
        assert "Название вакансии должно быть непустой строкой" in str(e)

    # Тест некорректного URL
    try:
        Vacancy(title="Developer", url="invalid_url")
        assert False, "Ожидалась ошибка валидации URL"
    except ValueError as e:
        assert "URL вакансии должен начинаться с http:// или https://" in str(e)

    # Тест отрицательной зарплаты
    vacancy = Vacancy(
        title="Developer",
        url="https://hh.ru/vacancy/123",
        salary_from=-1000,
        salary_to=-500
    )
    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0

    # Тест None зарплаты
    vacancy = Vacancy(
        title="Developer",
        url="https://hh.ru/vacancy/123",
        salary_from=None,
        salary_to=None
    )
    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0

    print("✓ Валидация данных работает")


def test_avg_salary():
    """Тест расчета средней зарплаты"""
    print("🧪 Тест расчета средней зарплаты...")

    # Обе зарплаты указаны
    vacancy1 = Vacancy(
        title="Developer 1",
        url="https://hh.ru/vacancy/1",
        salary_from=100000,
        salary_to=150000
    )
    assert vacancy1.get_avg_salary() == 125000

    # Только зарплата от
    vacancy2 = Vacancy(
        title="Developer 2",
        url="https://hh.ru/vacancy/2",
        salary_from=120000,
        salary_to=None
    )
    assert vacancy2.get_avg_salary() == 120000

    # Только зарплата до
    vacancy3 = Vacancy(
        title="Developer 3",
        url="https://hh.ru/vacancy/3",
        salary_from=None,
        salary_to=180000
    )
    assert vacancy3.get_avg_salary() == 180000

    # Зарплата не указана
    vacancy4 = Vacancy(
        title="Developer 4",
        url="https://hh.ru/vacancy/4"
    )
    assert vacancy4.get_avg_salary() == 0.0

    print("✓ Расчет средней зарплаты работает")


def test_comparison_operators():
    """Тест операторов сравнения"""
    print("🧪 Тест операторов сравнения...")

    vacancy_low = Vacancy(
        title="Junior Developer",
        url="https://hh.ru/vacancy/1",
        salary_from=50000,
        salary_to=80000
    )

    vacancy_medium = Vacancy(
        title="Middle Developer",
        url="https://hh.ru/vacancy/2",
        salary_from=100000,
        salary_to=150000
    )

    vacancy_high = Vacancy(
        title="Senior Developer",
        url="https://hh.ru/vacancy/3",
        salary_from=200000,
        salary_to=250000
    )

    vacancy_same = Vacancy(
        title="Another Middle",
        url="https://hh.ru/vacancy/4",
        salary_from=100000,
        salary_to=150000
    )

    # Тест равенства
    assert vacancy_medium == vacancy_same
    assert not vacancy_low == vacancy_high

    # Тест неравенства
    assert vacancy_low != vacancy_high

    # Тест меньше
    assert vacancy_low < vacancy_medium
    assert vacancy_low < vacancy_high
    assert not vacancy_high < vacancy_low

    # Тест меньше или равно
    assert vacancy_low <= vacancy_medium
    assert vacancy_medium <= vacancy_same
    assert not vacancy_high <= vacancy_low

    # Тест больше
    assert vacancy_high > vacancy_medium
    assert vacancy_high > vacancy_low
    assert not vacancy_low > vacancy_high

    # Тест больше или равно
    assert vacancy_high >= vacancy_medium
    assert vacancy_medium >= vacancy_same
    assert not vacancy_low >= vacancy_high

    print("✓ Операторы сравнения работают")


def test_string_representation():
    """Тест строкового представления"""
    print("🧪 Тест строкового представления...")

    # Вакансия с зарплатой
    vacancy_with_salary = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
        employer="Tech Corp"
    )

    string_repr = str(vacancy_with_salary)
    assert "Python Developer" in string_repr
    assert "Tech Corp" in string_repr
    assert "от 100000" in string_repr
    assert "до 150000" in string_repr
    assert "RUR" in string_repr
    assert "https://hh.ru/vacancy/123" in string_repr

    # Вакансия без зарплаты
    vacancy_no_salary = Vacancy(
        title="Java Developer",
        url="https://hh.ru/vacancy/456",
        employer="Bank Inc"
    )

    string_repr = str(vacancy_no_salary)
    assert "Java Developer" in string_repr
    assert "Bank Inc" in string_repr
    assert "Зарплата не указана" in string_repr
    assert "https://hh.ru/vacancy/456" in string_repr

    print("✓ Строковое представление работает")


def test_to_dict():
    """Тест преобразования в словарь"""
    print("🧪 Тест преобразования в словарь...")

    vacancy = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
        description="Backend development",
        requirements="Python 3+",
        employer="Tech Company"
    )

    vacancy_dict = vacancy.to_dict()

    assert vacancy_dict['title'] == "Python Developer"
    assert vacancy_dict['url'] == "https://hh.ru/vacancy/123"
    assert vacancy_dict['salary_from'] == 100000
    assert vacancy_dict['salary_to'] == 150000
    assert vacancy_dict['currency'] == "RUR"
    assert vacancy_dict['description'] == "Backend development"
    assert vacancy_dict['requirements'] == "Python 3+"
    assert vacancy_dict['employer'] == "Tech Company"

    print("✓ Преобразование в словарь работает")


def test_from_dict():
    """Тест создания из словаря"""
    print("🧪 Тест создания из словаря...")

    vacancy_data = {
        'title': 'Data Scientist',
        'url': 'https://hh.ru/vacancy/789',
        'salary_from': 150000,
        'salary_to': 200000,
        'currency': 'RUR',
        'description': 'ML development',
        'requirements': 'Python, ML, SQL',
        'employer': 'AI Company'
    }

    vacancy = Vacancy.from_dict(vacancy_data)

    assert vacancy.title == "Data Scientist"
    assert vacancy.url == "https://hh.ru/vacancy/789"
    assert vacancy.salary_from == 150000
    assert vacancy.salary_to == 200000
    assert vacancy.currency == "RUR"
    assert vacancy.description == "ML development"
    assert vacancy.requirements == "Python, ML, SQL"
    assert vacancy.employer == "AI Company"

    print("✓ Создание из словаря работает")


def test_from_dict_minimal():
    """Тест создания из словаря с минимальными данными"""
    print("🧪 Тест создания из словаря с минимальными данными...")

    vacancy_data = {
        'title': 'Developer',
        'url': 'https://hh.ru/vacancy/111'
    }

    vacancy = Vacancy.from_dict(vacancy_data)

    assert vacancy.title == "Developer"
    assert vacancy.url == "https://hh.ru/vacancy/111"
    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0
    assert vacancy.currency == ""
    assert vacancy.description == ""
    assert vacancy.requirements == ""
    assert vacancy.employer == ""

    print("✓ Создание из словаря с минимальными данными работает")


def test_cast_to_object_list():
    """Тест преобразования списка словарей в список объектов"""
    print("🧪 Тест преобразования списка словарей в список объектов...")

    vacancies_data = [
        {
            'name': 'Python Developer',
            'alternate_url': 'https://hh.ru/vacancy/1',
            'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'},
            'snippet': {'responsibility': 'Backend development', 'requirement': 'Python 3+'},
            'employer': {'name': 'Tech Company'}
        },
        {
            'name': 'Java Developer',
            'alternate_url': 'https://hh.ru/vacancy/2',
            'salary': None,
            'snippet': {'responsibility': '', 'requirement': ''},
            'employer': {'name': 'Bank Corp'}
        },
        {
            'name': 'Data Scientist',
            'alternate_url': 'https://hh.ru/vacancy/3',
            'salary': {'from': None, 'to': 200000, 'currency': 'RUR'},
            'snippet': {'responsibility': 'ML models', 'requirement': 'Python, SQL'},
            'employer': {'name': 'AI Labs'}
        }
    ]

    vacancies = Vacancy.cast_to_object_list(vacancies_data)

    assert len(vacancies) == 3

    # Проверяем первую вакансию
    assert vacancies[0].title == "Python Developer"
    assert vacancies[0].url == "https://hh.ru/vacancy/1"
    assert vacancies[0].salary_from == 100000
    assert vacancies[0].salary_to == 150000
    assert vacancies[0].currency == "RUR"
    assert vacancies[0].description == "Backend development"
    assert vacancies[0].requirements == "Python 3+"
    assert vacancies[0].employer == "Tech Company"

    # Проверяем вторую вакансию (без зарплаты)
    assert vacancies[1].title == "Java Developer"
    assert vacancies[1].url == "https://hh.ru/vacancy/2"
    assert vacancies[1].salary_from == 0
    assert vacancies[1].salary_to == 0
    assert vacancies[1].currency == ""
    assert vacancies[1].employer == "Bank Corp"

    # Проверяем третью вакансию (только зарплата до)
    assert vacancies[2].title == "Data Scientist"
    assert vacancies[2].url == "https://hh.ru/vacancy/3"
    assert vacancies[2].salary_from == 0
    assert vacancies[2].salary_to == 200000
    assert vacancies[2].currency == "RUR"
    assert vacancies[2].description == "ML models"
    assert vacancies[2].requirements == "Python, SQL"
    assert vacancies[2].employer == "AI Labs"

    print("✓ Преобразование списка словарей работает")


def test_properties():
    """Тест свойств (properties)"""
    print("🧪 Тест свойств (properties)...")

    vacancy = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
        description="Test description",
        requirements="Test requirements",
        employer="Test Company"
    )

    # Проверяем, что свойства доступны только для чтения
    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.currency == "RUR"
    assert vacancy.description == "Test description"
    assert vacancy.requirements == "Test requirements"
    assert vacancy.employer == "Test Company"

    print("✓ Свойства работают корректно")


def run_all_tests():
    """Запуск всех тестов"""
    print("🚀 Запуск тестов для класса Vacancy\n")

    tests = [
        test_vacancy_creation,
        test_vacancy_creation_minimal,
        test_vacancy_validation,
        test_avg_salary,
        test_comparison_operators,
        test_string_representation,
        test_to_dict,
        test_from_dict,
        test_from_dict_minimal,
        test_cast_to_object_list,
        test_properties,
    ]

    failed_tests = []

    for test_func in tests:
        try:
            test_func()
            print(f"✅ {test_func.__name__} - ПРОЙДЕН\n")
        except Exception as e:
            print(f"❌ {test_func.__name__} - ПРОВАЛЕН: {e}\n")
            failed_tests.append(test_func.__name__)

    # Финальный отчет
    print("=" * 50)
    if failed_tests:
        print(f"❌ ПРОВАЛЕНО: {len(failed_tests)} тестов")
        for test_name in failed_tests:
            print(f"   - {test_name}")
    else:
        print("🎉 ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()