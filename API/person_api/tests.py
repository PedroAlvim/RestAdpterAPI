from typing import Any

from django.db import transaction
from django.test import TestCase

from .models import University, Domain, WebPages


# Create your tests here.

class TestUniversity(TestCase):
    def print_db(self):
        print('University: {}'.format(University.objects.all()))
        print('Domains: {}'.format(Domain.objects.all()))
        print('WebPages: {}'.format(WebPages.objects.all()), '\n')

    def test_saving_old(self):
        try:
            with transaction.atomic():

                unifei = self.update_or_create(name='Universidade Federal de Itajubá', country='Brazil',
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

                obj = self.update_or_create(university_name, country, new_domains, new_web_pages, new_alpha_two_code,
                                            new_state_province)

                obj.save()
                self.print_db()
                obj.delete()
        finally:
            self.print_db()

    def test_creating_correct(self):
        domains = ['unifei.edu.br']
        web_pages = ['www.unifei.edu.br', 'www.unifei.com.ar']

        name = 'unifei'
        country = 'brasil'
        state_province = None
        alpha_two_code = 'BR'

        a = self.create_if_not_exist(name, country, alpha_two_code, domains, web_pages, state_province)
        self.print_db()
        a = self.create_if_not_exist(name, country, alpha_two_code, domains, web_pages, state_province)
        self.print_db()

    def create_if_not_exist(self, name: str, country: str, alpha_two_code: str, domains: list[str],
                            web_pages: list[str], state_province: str = None) -> tuple[Any, bool]:

        already_exist = University.objects.filter(domains__domain__in=domains, name=name,
                                                  web_pages__page__in=web_pages,
                                                  country=country, alpha_two_code=alpha_two_code,
                                                  state_province=state_province)
        if already_exist:
            return already_exist, False
        else:
            obj = University.objects.create(name=name,
                                            country=country,
                                            alpha_two_code=alpha_two_code,
                                            state_province=state_province)
            for domain in domains:
                Domain.objects.create(domain=domain, university=obj)
            for page in web_pages:
                WebPages.objects.create(page=page, university=obj)
        return obj, True
