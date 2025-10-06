from src.json_storage import JSONStorage
import json
import os
from tests.conftest import cleanup_file, create_test_vacancy

def test_init_default_file():
    cleanup_file("vacancies.json")

    storage = JSONStorage()
    assert storage._filename == "vacancies.json"
    assert os.path.exists("vacancies.json")

    with open("vacancies.json", 'r', encoding='utf-8') as f:
        content = json.load(f)
        assert content == []

    cleanup_file("vacancies.json")


def test_init_custom_file():

    test_filename = "test_custom.json"
    cleanup_file(test_filename)

    storage = JSONStorage(test_filename)
    assert storage._filename == test_filename
    assert os.path.exists(test_filename)

    cleanup_file(test_filename)


def test_add_and_get_vacancies():

    test_file = "test_add_get.json"
    cleanup_file(test_file)

    storage = JSONStorage(test_file)

    vacancy1 = create_test_vacancy("Python Developer", "Tech Company")
    vacancy2 = create_test_vacancy("Java Developer", "Bank Corp")

    storage.add_vacancy(vacancy1)
    storage.add_vacancy(vacancy2)

    vacancies = storage.get_vacancies()
    assert len(vacancies) == 2
    assert vacancies[0].title == "Python Developer"
    assert vacancies[1].title == "Java Developer"
    cleanup_file(test_file)

def test_duplicate_prevention():

    test_file = "test_duplicates.json"
    cleanup_file(test_file)

    storage = JSONStorage(test_file)

    vacancy = create_test_vacancy("Python Developer", "Same Company")

    storage.add_vacancy(vacancy)
    storage.add_vacancy(vacancy)

    vacancies = storage.get_vacancies()
    assert len(vacancies) == 1

    cleanup_file(test_file)

def test_delete_vacancy():

    test_file = "test_delete.json"
    cleanup_file(test_file)

    storage = JSONStorage(test_file)

    vacancy1 = create_test_vacancy("Python Developer", "Company A")
    vacancy2 = create_test_vacancy("Java Developer", "Company B")

    storage.add_vacancy(vacancy1)
    storage.add_vacancy(vacancy2)

    storage.delete_vacancy(vacancy1)

    vacancies = storage.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].title == "Java Developer"

    cleanup_file(test_file)