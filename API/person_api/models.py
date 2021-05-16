import warnings
from typing import Optional

from django.db import models


# Create your models here.


class Domain(models.Model):

    domain = models.CharField(max_length=64)
    university = models.ForeignKey('University', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='domains')

    def __str__(self):
        return self.domain


class WebPages(models.Model):
    page = models.URLField()
    university = models.ForeignKey('University', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='web_pages')

    def __str__(self):
        return self.page


class University(models.Model):
    country = models.CharField(max_length=32)
    alpha_two_code = models.CharField(max_length=2)
    name = models.CharField(max_length=132)
    state_province = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.country)

    @classmethod
    def create_if_not_exist(cls, name: str, country: str, alpha_two_code: str, domains: list[str],
                            web_pages: list[str], state_province: str = None) -> tuple['University', bool]:

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

            obj.save()
        return obj, True

    @staticmethod
    def update_or_create(name: str, country: str, domains: list[str], web_pages: list[str],
                         alpha_two_code: Optional[str] = None, state_province: Optional[str] = None):
        """
        !!! CASE of just name and country matters, if they were frozen attributes
         what isn't true in third party University API, there's no frozen id in University Objects
         2 Universities can have the same name, but they can be different.
        """
        warnings.warn("update_or_create() is deprecated; use create_if_not_exist().", DeprecationWarning)

        obj, created = University.objects.update_or_create(name=name,
                                                           country=country,
                                                           defaults={'alpha_two_code': alpha_two_code,
                                                                     'state_province': state_province})
        if not created:
            print('Updating {.name}'.format(obj), '\n')

        # updating existing domains with the new ones
        for existing_domain in obj.domains.all():
            if existing_domain.domain not in domains:
                existing_domain.delete()
            else:
                domains.remove(existing_domain.domain)
        for domain in domains:
            Domain.objects.create(domain=domain, university=obj)

        # updating existing web_pages with the new ones
        for existing_web_page in obj.web_pages.all():
            if existing_web_page.page not in web_pages:
                existing_web_page.delete()
            else:
                web_pages.remove(existing_web_page.page)
        for page in web_pages:
            WebPages.objects.create(page=page, university=obj)

        return obj
