# -*- coding: utf-8 -*-
from django.contrib import admin
from website.models import Travel, Gallery, Photo

# Register your models here.
models = [Travel, Gallery, Photo]
admin.site.register(models)
