# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
# Django properties
from django.core.files.storage import get_storage_class
from django.conf import settings
from django.db import models
# Fields
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

SEASONS = (
('invierno','Invierno'),
('verano','Verano'),
('primavera','Primavera'),
('otoño','Otoño'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github = models.CharField(max_length=100)

class Travel(models.Model):
    title = models.CharField(max_length=200)
    text = RichTextField()
    date =  models.DateTimeField()
    country = CountryField(blank_label='(select country)')
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    geo = models.CharField(max_length=500, blank=True, null=True)    # Google Maps URL
    price = models.IntegerField()
    score = models.IntegerField()
    season = models.CharField(max_length=50, choices=SEASONS, default='verano')

    def __str__(self):
        return self.title

    __original_title = None
    __original_date = None

    def __init__(self, *args, **kwargs):
        super(Travel, self).__init__(*args, **kwargs)
        self.__original_title = self.title
        self.__original_date = self.date


    def save(self, *args, **kwargs):
        if self.__original_title != self.title or self.__original_date != self.date:
            static_storage = get_storage_class(settings.STATICFILES_STORAGE)()

            if not self.id:
                # Crear carpeta
                super(Travel, self).save(*args, **kwargs)
                os.mkdir(static_storage.location + '/img/travel/{date}_{title}'.format(date=self.date.strftime('%Y_%m_%d'), title=self.title), 0755)
            else:
                # Renombrar carpeta
                if self.__original_date and self.__original_title and static_storage.exists('img/travel/{date}_{title}'.format(date=self.__original_date.strftime('%Y_%m_%d'), title=self.__original_title)):
                    os.rename(static_storage.location + '/img/travel/{date}_{title}/'.format(date=self.__original_date.strftime('%Y_%m_%d'), title=self.__original_title),
                            static_storage.location + '/img/travel/{date}_{title}/'.format(date=self.date.strftime('%Y_%m_%d'), title=self.title))
                else:
                    os.mkdir(static_storage.location + '/img/travel/{date}_{title}'.format(date=self.date.strftime('%Y_%m_%d'), title=self.title), 0755)
                    super(Travel, self).save(*args, **kwargs)
        else:
            super(Travel, self).save(*args, **kwargs)
