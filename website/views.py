# from django.shortcuts import render
# from django.http import HttpResponse
# from .models import Customers
# # Create your views here.


# def home(request):
#     coupons = Customers.objects.all()[:5]
#     output = '<br>'.join([str(c.last_name) for c in coupons])
#     return HttpResponse(output)

# from django.db import connection
# cursor = connection.cursor()
# cursor.execute('''SELECT count(*) FROM Orders WHERE order_id<10''')
# row = cursor.fetchall() #fecthone()
# print(row)

# or
        # SELECT count(*) as all_count,
        # count(*) FILTER(WHERE vote = 'yes') as yes_count
        # FROM people_person;

from django.shortcuts import render
from .models import Foods
from .models import Orders
from .models import Restaurants
from .models import Platforms
from django.db import connection
from django.http import HttpResponse



def home(request):


    # for d in Student.objects.raw('SELECT * FROM student_student'):
    #     print(d)
    # foodrest = Foods.objects.get(id=1)
    # get Post object that the Attending object have in ForeignKey field
    SD_DATA = Foods.objects.all()
    sql='SELECT * FROM Foods'
    SD_DATA = Foods.objects.raw(sql)[0:3]
    # print(SD_DATA)
    # print(connection.queries)
    return render(request,'home.html',{'data': SD_DATA})

def insert(request):
        if request.method == 'POST':
            if request.POST.get('name') and request.POST.get('id'):
                with connection.cursor() as cursor:
                # post = Platforms()
                # post.platform_id= request.POST.get('id')
                # post.platform_name= request.POST.get('name')
                    # cursor = connection['my_db_alias'].cursor()
                    cursor.execute('INSERT into Platforms(platform_id, platform_name) VALUES (%s, %s)', [request.POST.get('id'), request.POST.get('name')])

                    # cursor.fetchall()
                    # post.save()
                
                    return render(request, 'insert.html')  

        else:
                return render(request,'insert.html')

def update(request):
        if request.method == 'POST':
            if request.POST.get('cust_id') and request.POST.get('price'):
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE Orders SET \
                         price = %s WHERE order_id = 1",  [request.POST.get('price')])
                    return render(request, 'update.html')  

        else:
                return render(request,'update.html')


def delete(request):
        if request.method == 'POST':
            if request.POST.get('order_id'):
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM Orders \
                         WHERE order_id = %s",  [request.POST.get('order_id')])
                    return render(request, 'delete.html')  

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

