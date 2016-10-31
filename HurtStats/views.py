from django.shortcuts import render

# Create your views here.
from HurtStats.data_provider import get_data, get_clans


def index(request):
    data = get_data()
    clans = get_clans(data)
    return render(request,"index.html", {"data":data, "clans":clans})