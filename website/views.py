from django.shortcuts import render
from django.http import HttpResponse
from .models import Customers
# Create your views here.


def home(request):
    coupons = Customers.objects.all()[:5]
    output = '<br>'.join([str(c.last_name) for c in coupons])
    return HttpResponse(output)
