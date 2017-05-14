from django.shortcuts import render
from show.models import Information
from bson.json_util import dumps

def index(request):
    _id, title, address, price, img, hostPic, hostName, hostGender = [], [], [], [], [], [], [], []
    count = 0
    for var in Information.objects:
        # get data from database
        _id.append(var._id)
        title.append(var.title)
        address.append(var.address)
        price.append(var.price)
        img.append(var.img)
        hostPic.append(var.hostPic)
        hostName.append(var.hostPic)
        hostGender.append(var.hostGender)
        count += 1
    return render(request, 'index.html', {'_id': dumps(_id),
        'title': dumps(title),
        'address': dumps(address),
        'price': dumps(price),
        'img': dumps(img),
        'hostPic': dumps(hostPic),
        'hostName': dumps(hostName),
        'hostGender': dumps(hostGender),
        'count': range(count)
    })

