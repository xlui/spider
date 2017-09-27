from django.shortcuts import render
from .models import Information


def index(request):
    title = Information.objects[0].title
    return render(request, 'index.html', {'title': title})
