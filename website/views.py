from django.shortcuts import render

from .models import Foods
from .models import Orders
from .models import Restaurants
from .models import Customers
from .models import Platforms
from django.db import connection
from django.http import HttpResponse
from django.template import loader
from .forms import RestaurantSearchForm
# def home(request):


#     SD_DATA = Foods.objects.all()
#     sql='SELECT * FROM Foods'
#     SD_DATA = Foods.objects.raw(sql)[0:3]
#     # print(SD_DATA)
#     # print(connection.queries)
#     return render(request,'home.html',{'data': SD_DATA})

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

def insert(request):
        # template = loader.get_template('insert.html')
        if request.method == 'POST':
            if request.POST.get('name') and request.POST.get('id'):
                with connection.cursor() as cursor:
                # post = Platforms()
                # post.platform_id= request.POST.get('id')
                # post.platform_name= request.POST.get('name')
                    # cursor = connection['my_db_alias'].cursor()
                    cursor.execute('INSERT into Platforms(platform_id, platform_name) VALUES (%s, %s)', [request.POST.get('id'), request.POST.get('name')])
                    cursor.execute('SELECT * \
                                    FROM Platforms;')
                    # cursor.fetchall()
                    # post.save()
                    query = cursor.fetchall()
                    return render(request, 'insert.html', {'query': query})  

        else:
                return render(request,'insert.html')

def update(request):
        if request.method == 'POST':
            if request.POST.get('cust_id') and request.POST.get('price'):
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE Orders SET \
                         price = %s WHERE order_id = 1",  [request.POST.get('price')])
                    cursor.execute('SELECT * FROM Orders WHERE order_id=1;')
                    query = cursor.fetchall()
                    return render(request, 'update.html', {'query': query})  

        else:
                return render(request,'update.html')


def delete(request):
        if request.method == 'POST':
            if request.POST.get('order_id'):
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM Orders \
                         WHERE order_id = %s",  [request.POST.get('order_id')])
                    cursor.execute('SELECT * FROM Orders WHERE order_id<=%s+10 and order_id>=%s-10;', [request.POST.get('order_id'), request.POST.get('order_id')])
                    query = cursor.fetchall()
                    return render(request, 'delete.html', {'query': query})  

        else:
                return render(request,'delete.html')


def search(request):
        if request.method == 'POST':
            if request.POST.get('cust_id') and request.POST.get('price'):
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE Orders SET \
                         price = %s WHERE order_id = 1",  [request.POST.get('price')])
                    return render(request, 'update.html')  

        else:
                return render(request,'update.html')


# SELECT o.Date, COUNT(o.Order_ID)
# FROM Customers c JOIN Orders o USING(Customer_Id)
# WHERE c.Last_Name LIKE "C%" 
# GROUP BY o.Date
# ORDER BY o.Date;

def advance1(request):

    cursor = connection.cursor()
    try:
        cursor.execute('SELECT o.Date, COUNT(o.Order_ID) \
        FROM Customers AS c JOIN Orders AS o USING(customer_id) \
        WHERE c.Last_Name LIKE "C%" \
        GROUP BY o.Date \
        ORDER BY o.Date;')
    finally:
        cursor.close()
    query = cursor.fetchall()
    return render(request, 'advance1.html',{'query': query})

def advance2(request):

    cursor = connection.cursor()
    try:
        cursor.execute('SELECT r.Restaurant_ID, r.Name\
        FROM Foods f JOIN Restaurants r USING(Restaurant_ID)\
        WHERE f.Price <= 5 and r.Cuisine_Type LIKE "%Ice Cream%"\
        UNION\
        SELECT r.Restaurant_ID, r.Name\
        FROM Foods f JOIN Restaurants r USING(Restaurant_ID)\
        WHERE f.Price <= 15 and r.Cuisine_Type LIKE "%Burger%"\
        ORDER BY Name;')
    finally:
        cursor.close()
    query = cursor.fetchall()
    return render(request, 'advance2.html',{'query': query})


