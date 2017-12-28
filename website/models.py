# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from future.utils import native
from future.builtins import str
from django.core.files.images import ImageFile

import os, sys, io

# Django properties
from django.core.files.storage import FileSystemStorage, get_storage_class, default_storage
from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings
from django.db import models

# Fields
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from zipfile import ZipFile
from django.db.models.signals import post_delete


fs = FileSystemStorage(location=settings.STATIC_ROOT)

UPLOADS_GALLERY_DIRECTORY = 'travels'

class Gallery(models.Model):
    zipfile = models.FileField(verbose_name="Zip File", upload_to=UPLOADS_GALLERY_DIRECTORY,
        help_text="Upload a zip file containing images, and they'll be imported into this gallery.")

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"


    def save(self, *args, **kwargs):
        super(Gallery, self).save(*args, **kwargs)
        if self.zipfile:
            from zipfile import ZipFile
            zip_file = ZipFile(self.zipfile)
            for name in zip_file.namelist():
                data = zip_file.read(name)
                try:
                    from PIL import Image
                    image = Image.open(io.BytesIO(data))
                    image.load()
                    image = Image.open(io.BytesIO(data))
                    image.verify()
                except ImportError:
                    pass
                except:
                    continue
                path = os.path.join(settings.MEDIA_ROOT, UPLOADS_GALLERY_DIRECTORY, native(str(name, errors="ignore")))
                img_tmp_path = default_storage.save(path, ContentFile(data))

                photo = Photo()
                photo.image.save(os.path.basename(img_tmp_path), File(open(img_tmp_path)))
                photo.album = os.path.splitext(os.path.split(zip_file.filename)[1])[0]
                photo.save()

                os.remove(img_tmp_path)
            zip_file.close()
            self.zipfile.delete(save=True)

class Photo(models.Model):
    image = models.ImageField(upload_to=UPLOADS_GALLERY_DIRECTORY)
    album = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    banner = models.BooleanField(default=False)

    def __str__(self):
        return ("{}, {}").format(self.album, self.description)


class Travel(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    text = RichTextField()
    date =  models.DateTimeField()
    country = CountryField(blank_label='(select country)')
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    geo = models.CharField(verbose_name=("Google Map"), max_length=500, blank=True, null=True,
        help_text="Insertar el enlace del mapa embebido de Google MyMaps.")
    price = models.IntegerField()
    score = models.IntegerField()
    season = models.CharField(max_length=50, default='verano', choices=(('invierno','Invierno'),('verano','Verano'),('primavera','Primavera'),('otoño','Otoño')))
    gallery = models.ManyToManyField(Photo)


    def __str__(self):
        return self.title
