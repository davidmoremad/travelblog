# -*- coding: utf-8 -*-
from django.contrib import admin
from website.models import Travel, Profile

# Register your models here.
models = [Travel, Profile]
admin.site.register(models)
