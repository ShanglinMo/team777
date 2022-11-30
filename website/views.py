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


# SELECT o.Date, COUNT(o.Order_ID)
# FROM Customers c JOIN Orders o USING(Customer_Id)
# WHERE c.Last_Name LIKE "C%"
# GROUP BY o.Date
# ORDER BY o.Date;

# def advance1(request):

#     cursor = connection.cursor()
#     try:
#         cursor.execute('SELECT o.Date, COUNT(o.Order_ID) \
#         FROM Customers AS c JOIN Orders AS o USING(customer_id) \
#         WHERE c.Last_Name LIKE "C%" \
#         GROUP BY o.Date \
#         ORDER BY o.Date;')
#     finally:
#         cursor.close()
#     query = cursor.fetchall()
#     return render(request, 'advance1.html',{'query': query})
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



# def advance2(request):

#     cursor = connection.cursor()
#     try:
#         cursor.execute('SELECT r.Restaurant_ID, r.Name\
#         FROM Foods f JOIN Restaurants r USING(Restaurant_ID)\
#         WHERE f.Price <= 5 and r.Cuisine_Type LIKE "%Ice Cream%"\
#         UNION\
#         SELECT r.Restaurant_ID, r.Name\
#         FROM Foods f JOIN Restaurants r USING(Restaurant_ID)\
#         WHERE f.Price <= 15 and r.Cuisine_Type LIKE "%Burger%"\
#         ORDER BY Name;')
#     finally:
#         cursor.close()
#     query = cursor.fetchall()
#     return render(request, 'advance2.html',{'query': query})


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

# START TRANSACTION;
# SELECT @orderNumber:=MAX(orderNumber)+1
# FROM Orders;

# SELECT cust_id
# FROM (SELECT c.customer_id as cust_id, count(order_id) as cnt
# FROM Customers c JOIN Orders o Using(Customer_Id)
# GROUP BY c.customer_id) as temp
# WHERE cnt>10;

# SELECT hoover_customer_id
# FROM Customers
# WHERE customer_id is cust_id and Address LIKE ‘%Hoover%’;

# INSERT INTO Orders(Order_ID, Coupon_ID, Customer_ID, Item_ID_List, Price, Date)
# VALUES(@orderNumber, null, hoover_customer_id, [11014, 10986], 0, ‘2022-12-24’);

# COMMIT;
def transaction(request):
        if request.method == 'POST':
            if request.POST.get('cust_id') and request.POST.get('price'):
                with connection.cursor() as cursor:
                    cursor.execute("START TRANSACTION;")
                    # get the orderNumber to add the new order
                    cursor.execute("SELECT @order_ID:=MAX(order_ID)+1\
                                    FROM Orders;")

                    #get the customer who ordered the most
                    cursor.execute("SELECT @cust_id:=c.Customer_ID, @cnt:=count(order_id)\
                                    FROM Customers c JOIN Orders o USING(Customer_Id)\
                                    WHERE c.Address LIKE '%Hoover, AL%'\
                                    GROUP BY c.Customer_ID\
                                    ORDER BY count(order_id) desc\
                                    limit 1;")

                    cursor.execute("INSERT INTO Orders(Order_ID, Coupon_ID, Customer_ID, Item_ID_List, Price, Date)\
                                   VALUES(@order_ID, null, @cust_id,'[11014]', 0, '2022-12-24');")
``
                    # cusror.execute("IF cnt > 15 THEN UPDATE Orders SET Item_ID_List = '[11014, 10986]';\
                    #                 ELSE UPDATE Orders SET Item_ID_List = '[11014]';")
                    # cursor.execute("IF @cnt > 15 THEN\
                    #                 SET Item_ID_List = '[11014, 10986]';")

                    cursor.execute('SELECT * FROM Orders WHERE order_ID=@order_ID;')
                    query = cursor.fetchall()
                    return render(request, 'transaction.html', {'query': query})

        else:
                return render(request,'transaction.html')

