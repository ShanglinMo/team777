from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Customers
# Create your views here.


def home(request):
    template = loader.get_template('home.html')
    customers = Customers.objects.all().values()
    context = {
        'customers': customers,
    }
    return HttpResponse(template.render({}, request))
    #return HttpResponse(template.render(context, request))
