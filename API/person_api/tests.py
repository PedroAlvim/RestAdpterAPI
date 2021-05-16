"""
To proper run django TestCase test on Pycharm interface you need to configure django support for pycharm in:
File | Settings | Languages & Frameworks | Django
"""

from django.test import TestCase

from .models import University, Domain, WebPages


class TestUniversity(TestCase):

    @staticmethod
    def print_db():
        print('University: {}'.format(University.objects.all()))
        print('Domains: {}'.format(Domain.objects.all()))
        print('WebPages: {}'.format(WebPages.objects.all()), '\n')

    def test_creating_correct(self):
        domains = ['unifei.edu.br']
        web_pages = ['www.unifei.edu.br', 'www.unifei.com.ar']

        name = 'unifei'
        country = 'brasil'
        state_province = None
        alpha_two_code = 'BR'

        University.create_if_not_exist(name, country, alpha_two_code, domains, web_pages, state_province)
        self.print_db()
        University.create_if_not_exist(name, country, alpha_two_code, domains, web_pages, state_province)
        self.print_db()

    def test_saving_deprecated(self):
        unifei = University.update_or_create(name='Universidade Federal de Itajubá', country='Brazil',
                                             alpha_two_code='BR',
                                             state_province=None, domains=['unifei.edu.br'],
                                             web_pages=['www.unifei.com.br', 'www.unifei.edu.br'])
        unifei.save()
        self.print_db()

        university_name = 'Universidade Federal de Itajubá'
        country = 'Brazil'

        new_alpha_two_code = 'AR'
        new_state_province = 'GH'
        new_domains = ['unifei.edu.ar']
        new_web_pages = ['www.unifei.com.br', 'www.unifei.edu.ar']

        obj = University.update_or_create(university_name, country, new_domains, new_web_pages,
                                          new_alpha_two_code,
                                          new_state_province)

        obj.save()
        self.print_db()
        obj.delete()
