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
from django.shortcuts import render


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
            if request.POST.get('order_id') and request.POST.get('price'):
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE Orders SET \
                         price = %s WHERE order_id = %s",  [request.POST.get('price'),request.POST.get("order_id")])
                    cursor.execute('SELECT * FROM Orders WHERE order_id=%s;',[request.POST.get("order_id")])
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


def advance1(request):
# template = loader.get_template('insert.html')
    if request.method == 'POST':
        if request.POST.get('Last_Name') and request.POST.get("First_Name"):
            with connection.cursor() as cursor:
                cursor.execute('SELECT o.Date, COUNT(o.Order_ID) as order_c\
                FROM Customers AS c JOIN Orders AS o USING(customer_id) \
                WHERE c.Last_Name LIKE %s and c.First_Name LIKE %s\
                GROUP BY o.Date \
                ORDER BY o.Date;',[request.POST.get("Last_Name"),request.POST.get("First_Name")])
                query = cursor.fetchall()
                return render(request, 'advance1.html', {'query': query})

    else:
            return render(request,'advance1.html')




def advance2(request):
    if request.method == 'POST':
        if request.POST.get('Price1') and request.POST.get('Price2') and request.POST.get("Cuisine_Type1") and request.POST.get('Cuisine_Type2'):
            with connection.cursor() as cursor:
                price1 = request.POST.get("Price1")
                # print(type(price1))
                price2 = request.POST.get("Price2")
                cuisine_type1 = '%' + request.POST.get("Cuisine_Type1") + '%'
                cuisine_type2 = '%' + request.POST.get("Cuisine_Type2") + '%'
                cursor.execute('SELECT r.Restaurant_ID, r.Name\
                FROM Foods f JOIN Restaurants r USING(Restaurant_ID)\
                WHERE f.Price <= %s and r.Cuisine_Type LIKE %s\
                UNION\
                SELECT r.Restaurant_ID, r.Name\
                FROM Foods f JOIN Restaurants r USING(Restaurant_ID)\
                WHERE f.Price <= %s and r.Cuisine_Type LIKE %s\
                ORDER BY Name;',[price1,cuisine_type1,price2,cuisine_type2])
                query = cursor.fetchall()
                return render(request, 'advance2.html', {'query': query})
    else:
        return render(request,'advance2.html')

def transaction(request):
        with connection.cursor() as cursor:
                cursor.execute("call christmas();")
                cursor.execute("select * FROM Orders as O NATURAL JOIN Customers as C WHERE Date = '2024-01-01';")
                query = cursor.fetchall()
                return render(request, 'transaction.html', {'query': query})


def recommendation(request):
    if request.method == "POST":
        if request.POST.get("Customer_ID") and request.POST.get("price"):
            with connection.cursor() as cursor:
                customerID = request.POST.get("Customer_ID")
                cursor.execute('select Customer_ID,avg(Price) as avgPrice\
                                                     from Orders \
                                                     where Customer_ID = %s\
                                                     group by Customer_ID;',[customerID])
                customerInfo = cursor.fetchall()
                
                for c in customerInfo:
                    avgPrice = c[1]
                    if int(avgPrice) <= 10:
                        cursor.execute("select temp.Restaurant_ID, r.Name, r.Cuisine_Type, temp.Consumption_Level\
                                        from (select Restaurant_ID, Consumption_Level\
                                        from RestaurantConsumptionLevel\
                                        where Consumption_Level = 'Low'\
                                        ORDER BY RAND()\
                                        limit 5) as temp natural join Restaurants r;")
                        query = cursor.fetchall()
                        return render(request, 'recommendation.html', {'query': query})
                    elif int(avgPrice) > 10 and int(avgPrice) <= 20:
                        cursor.execute("select temp.Restaurant_ID, r.Name, r.Cuisine_Type, temp.Consumption_Level\
                                        from (select Restaurant_ID,Consumption_Level\
                                        from RestaurantConsumptionLevel\
                                        where Consumption_Level = 'Medium'\
                                        ORDER BY RAND()\
                                        limit 5) as temp natural join Restaurants r;")
                        query = cursor.fetchall()
                        return render(request, 'recommendation.html', {'query': query}) 
                    # avgPrice > 20
                    else: 
                        cursor.execute("select temp.Restaurant_ID, r.Name, r.Cuisine_Type, temp.Consumption_Level\
                                        from (select Restaurant_ID, Consumption_Level\
                                        from RestaurantConsumptionLevel\
                                        where Consumption_Level = 'High'\
                                        ORDER BY RAND()\
                                        limit 5) as temp natural join Restaurants r;")
                        query = cursor.fetchall()
                        return render(request, 'recommendation.html', {'query': query})  

        elif request.POST.get("Customer_ID") and request.POST.get("history"):
            with connection.cursor() as cursor:
                customerID = request.POST.get("Customer_ID") 
                cursor.execute('SELECT r.Cuisine_Type\
                                FROM easy_dinner.Orders o natural join easy_dinner.Restaurants r natural join easy_dinner.RestaurantConsumptionLevel rcl\
                                where Customer_ID = %s;',[customerID])
                cuisineType = cursor.fetchall()
                cuisineType = cuisineType[0][0]
                temp = ''.join(cuisineType)
                # temp = ', '.join(map(str, cuisineType))
                cuisine_type = temp.split(",")
                cuisine = max(cuisine_type,key=cuisine_type.count)
                cuisine_type = '%' + cuisine + '%'
                cursor.execute("select temp.Restaurant_ID, r.Name, r.Cuisine_Type, temp.Consumption_Level\
                                        from (select Restaurant_ID, Consumption_Level\
                                        from RestaurantConsumptionLevel\
                                        ORDER BY RAND()) as temp natural join Restaurants r\
                                        where lower(r.Cuisine_Type) like lower(%s)\
                                        limit 5;",[cuisine_type])
                query = cursor.fetchall()
                return render(request, 'recommendation.html', {'query': query}) 
        elif request.POST.get("Customer_ID") and request.POST.get("random"):
            with connection.cursor() as cursor:
                cursor.execute("select temp.Restaurant_ID, r.Name, r.Cuisine_Type, temp.Consumption_Level\
                                    from (select Restaurant_ID, Consumption_Level\
                                    from RestaurantConsumptionLevel\
                                    ORDER BY RAND()\
                                    limit 5) as temp natural join Restaurants r;")
                query = cursor.fetchall()
                return render(request, 'recommendation.html', {'query': query})  
        else:
            return render(request,"recommendation.html")
    else:
        return render(request,"recommendation.html")


def makeorder(request):
    print(1234556)
    a = request.method
    if request.method == 'POST':
        print(xyzzzz)
        if request.POST.get('orderItem'):
            print(34566)
            orderList = request.POST.getlist('orderItem')
            for x in orderList:
                print(x)
            return render(request, 'makeorder.html', {'orderList': orderList})

    else:
        return render(request,'makeorder.html')
    



