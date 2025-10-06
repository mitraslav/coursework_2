import pytest
from unittest.mock import patch, Mock
from src.hh_api import HeadHunterAPI

def test_init():
    api = HeadHunterAPI()

    assert api._base_url == "https://api.hh.ru/vacancies"
    assert api._headers == {'User-Agent': 'HH-User-Agent'}

def test_connect_success():
    api = HeadHunterAPI()

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = api._connect()

        assert result is True
        mock_get.assert_called_once_with(api._base_url, headers=api._headers, timeout=5)

def test_connect_failure():
    api = HeadHunterAPI()

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = api._connect()

        assert result is False

def test_get_vacancies_success():
    api = HeadHunterAPI()

    with patch.object(api, '_connect', return_value=True):
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'items': [
                    {'id': '1', 'name': 'Python Developer'},
                    {'id': '2', 'name': 'Java Developer'}
                ]
            }
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            vacancies = api.get_vacancies("Python", per_page=10)

            assert len(vacancies) == 2
            assert vacancies[0]['name'] == 'Python Developer'
            assert vacancies[1]['name'] == 'Java Developer'

def test_get_vacancies_connection_error():
    api = HeadHunterAPI()

    with patch.object(api, '_connect', return_value=False):
        with pytest.raises(ConnectionError, match='Не удалось подключиться к API HH.ru'):
            api.get_vacancies('Python')

