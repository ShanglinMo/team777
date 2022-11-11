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


# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
# def search(request):
#     SD_DATA = Foods.objects.all()
#     SD_DATA = Foods.objects.raw('SELECT * FROM Foods')[:10]
#     # you get to this "if" if the form has been filled by the user
#     if request.method == "POST":
#         # form = AttendanceForm(request.POST)
#         food = SD_DATA(request.POST)
#         if food.is_valid():
#             foodId = request.POST['item_id']
#             restaurant = request.POST['restaurant']
#             name = request.POST['name']
#             members = 
#             # members = Member.objects.filter(#here you do your filters as you already have the course, department and semester variables)
#             context = {'members': members}
#             return render(request, 'second_page.html', context)
#     # if the form hasn't been filled by the user you display the form
#     context = {'form': form}
#     return render(request, 'form_page.html', context)

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


# SELECT o.Date, COUNT(o.Order_ID)
# FROM Customers c JOIN Orders o USING(Customer_Id)
# WHERE c.Last_Name LIKE "C%" 
# GROUP BY o.Date
# ORDER BY o.Date;

def advanced(request):
    sql = 'SELECT o.Date, COUNT(o.Order_ID) \
        FROM Customers AS c JOIN Orders AS o USING(customer_id) \
        WHERE c.Last_Name LIKE "C%" \
        GROUP BY o.Date \
        ORDER BY o.Date;'
    cursor = connection.cursor()
    try:
        cursor.execute(sql, ['localhost'])
        row = cursor.fetchall()
    except Exception as e:
        cursor.close

    return render(request,'advance1.html',{'data': SD_DATA})