# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import Travel
from django.core.files.storage import get_storage_class
from django.conf import settings

def home(request):
    travels = Travel.objects.all()
    return render(request, 'index.html', {'travels':travels})

def travel_list(request):
    travels = Travel.objects.all().order_by('country')
    return render(request, 'travel/index.html', {'travels':travels})

def travel_detail(request, pk):
    travel = Travel.objects.get(pk=pk)

    travel.images = list()
    static_storage = get_storage_class(settings.STATICFILES_STORAGE)()
    img_dir = 'img/travel/{date}_{title}/'.format(date=travel.date.strftime('%Y_%m_%d'), title=travel.title)
    if static_storage.exists(img_dir):
        travel.images.extend([img_dir + x for x in static_storage.listdir(img_dir)[1]])
    return render(request, 'travel/detail.html', {'travel':travel})

def contact(request):
    return render(request, 'contact.html')
