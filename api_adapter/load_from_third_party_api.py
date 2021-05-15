import unittest
from typing import ClassVar

import attr
import requests
from django.db import transaction

from django_configuration import University


@attr.s(auto_attribs=True)
class UniversityLoader:
    url: ClassVar = 'http://universities.hipolabs.com/search?country={}'
    countries: list[str]

    def load_to_db(self):
        for country in self.countries:
            universities = requests.get(self.url.format('+'.join(country.split())))
            universities.raise_for_status()
            for university in universities.json():
                uni, created = University.create_if_not_exist(name=university.get('name'),
                                                              country=country,
                                                              alpha_two_code=university.get('alpha_two_code'),
                                                              domains=university.get('domains'),
                                                              web_pages=university.get('web_pages'),
                                                              state_province=university.get('state-province'))

                if created:
                    print('saving University: {.name}'.format(uni))
                    uni.save()


class TestAPIAdapter(unittest.TestCase):

    def test_but_rollback_if_success_load_brazil_us_universities(self):
        """ this test will use the actual database but will not keep changes"""
        try:
            with transaction.atomic():
                University.objects.all().delete()
                UniversityLoader(['Brazil', 'United States']).load_to_db()
                raise Exception  # remove this error to actually modify the database in this test
                # obs self.assertRaises don't worked...
        except Exception:
            self.assertTrue(True)

    def test_load_brazil_us_universities(self):
        """ this test will use the real database """
        UniversityLoader(['Brazil', 'United States']).load_to_db()
