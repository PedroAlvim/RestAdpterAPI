import unittest

import requests

MAIN_URL = 'http://127.0.0.1:8000/'

SEARCH_URL = 'search/?search='
UNIVERSITY_URL = 'universities/'


def get_request(url, params=None, **kwargs):
    try:
        response = requests.get(url, params, **kwargs)
    except Exception as e:
        raise ConnectionError('Check if you start the server with: python django runserver. Error: {}'.format(e))

    return response


def search_university_by_domain(text: str):
    return get_request(f'{MAIN_URL}{SEARCH_URL}{text}')


def get_university_by_key(key: int):
    return get_request(f'{MAIN_URL}{UNIVERSITY_URL}{key}')


def print_university(university: dict):
    print('-' * 11, 'University', '-' * 11, '\n',
          'id: {id}\n'
          'Name: {name}\n'
          'Country: {country}\n'
          'Country code: {alpha_two_code}\n'
          'Domains: {domains}\n'
          'Web Pages: {web_pages}\n'.format(**university))


class TestUniversityAPI(unittest.TestCase):
    unifei = {'id': 74,
              'name': 'Universidade Federal de Itajubá',
              'country': 'Brazil',
              'alpha_two_code': 'BR',
              'state_province': None,
              'domains': ['unifei.edu.br'],
              'web_pages': ['https://unifei.edu.br/']}

    def test_search(self):
        response = search_university_by_domain('unifei')
        self.assertIsNot(response.json(), [])

        print_university(response.json()[0])
        self.assertEqual(response.json()[0], self.unifei)

    def test_get_university_by_key(self):
        response = get_university_by_key(74)

        print_university(response.json())
        self.assertEqual(response.json(), self.unifei)
