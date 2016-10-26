from django.shortcuts import render

# Create your views here.
from HurtStats.data_provider import get_data


def index(request):
    return render(request,"index.html", {"data":get_data()})