from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Customers
from .models import Restaurants
from .forms import RestaurantSearchForm
# Create your views here.


def home(request):
    template = loader.get_template('home.html')
    customers = Customers.objects.all().values()
    context = {
        'customers': customers,
    }
    return HttpResponse(template.render({}, request))
    #return HttpResponse(template.render(context, request))


def restaurant(request):
    template = loader.get_template('restaurant.html')
    restaurants = Restaurants.objects.raw('Select * from Restaurants')
    form = RestaurantSearchForm(request.POST or None)
    context = {
        'restaurants': restaurants,
        'form': form,
    }
    #if user does search
    if request.method == 'POST':
        name = '%'+ form['name'].value() + '%'
        cuisine_type = '%' + form['cuisine_type'].value() + '%'
        #restaurants = Restaurants.objects.filter( name__icontains=form['name'].value(), cuisine_type__icontains=form['cuisine_type'].value())
        restaurants = Restaurants.objects.raw('Select * from Restaurants where lower(Name) like lower(%s) and lower(Cuisine_Type) like lower(%s)', tuple([name, cuisine_type]))

        context = {
        'form': form,
        'restaurants': restaurants,
        }

    return HttpResponse(template.render(context, request))
