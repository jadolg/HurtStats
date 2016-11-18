from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from HurtStats.data_provider import get_data, get_clans
from untitled2.settings import ADMIN_IPS


def index(request):
    data = get_data()
    clans = get_clans(data)
    ip = request.META.get('REMOTE_ADDR', None)


    return render(request,"index.html", {"data":data, "clans":clans})


def index_admin(request):
    data = get_data()
    ip = request.META.get('REMOTE_ADDR', None)

    isadmin = ip in ADMIN_IPS

    if not isadmin:
        return HttpResponseRedirect('/')

    return render(request,"index_admin.html", {"data":data, "isadmin":isadmin})