import json
from django.shortcuts import render
from Show.models import Data


def index(request):
    data = {}
    for var in Data.objects:
        data.setdefault('title', []).append(var.title)
        data.setdefault('address', []).append(var.address)
        data.setdefault('price', []).append(var.price)
        data.setdefault('img', []).append(var.img)
        data.setdefault('host_pic', []).append(var.host_pic)
        data.setdefault('host_gender', []).append(var.host_gender)
    total = Data.objects.count()
    return render(request, 'index.html', {'total':total, 'data': json.dumps(data)})
