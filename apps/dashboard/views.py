from django.shortcuts import render, HttpResponse, redirect

# import object Class(es) from models.py
from ..users.models import *

# import messages to use flask error messaging
from django.contrib import messages

# Inside your app's views.py file
from django.core.urlresolvers import reverse


# /dashboard - display "placeholder to display a normal user's dashboard
def dashboard(request):
    print "**** in dashboard route (for normal users)"
    context = {
        "users": User.objects.all()
        }
    return render(request, 'dashboard/index.html', context)


# /dashboard/admin - display "placeholder to display an admin's dashboard
def admin(request):
    print "**** in dashboard admin route"
    context = {
        "users": User.objects.all()
        }
    return render(request, 'dashboard/admin.html', context)
