from django.shortcuts import render
from .models import orders
from cart.models import carts
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection, transaction
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from comments.views import makereview
from .models import orders
# Create your views here.
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def checkorder(request):
    if request.method == 'GET':
        return render(request, 'order/searchorder.html', )
        # list1 = orders.objects.filter(userId=request.user.id)
        # list2 = carts.objects.filter(userId=request.user.id,status = "InHouse")
        # list1.union(list2).order_by('shipId')
        # print(list1)
        # return HttpResponseRedirect('/browsePro/success/')
        #list1 = orders.objects.select_related("ship")
       # for x in list1:
            #print(x)
        #print(list1)
       # cursor = connection.cursor()
       # cursor.execute('''SELECT order_orders.shipid, order_orders.status,
       #                order_orders.addressx, order_orders.addressy, cart_carts.productid, cart_carts.count
       #                 from order_orders INNER JOIN cart_carts on cart_carts.ship_id = order_orders.shipid
       #                WHERE order_orders.userid = %s''', str(request.user.id))
       # row = dictfetchall(cursor)
       # return render(request,'order/checkorder.html',{'list':row,'number':len(row)})
    if request.method == 'POST':
        search = request.POST.dict()
        print(search)
        for (x, y) in search.items():
            if "showlist" in x:
                cursor = connection.cursor()
                cursor.execute('''SELECT order_orders.shipid, order_orders.status,
                               order_orders.addressx, order_orders.addressy, cart_carts.productid, cart_carts.count
                                from order_orders INNER JOIN cart_carts on cart_carts.ship_id = order_orders.shipid
                               WHERE order_orders.userid = %s''', str(request.user.id))
                row = dictfetchall(cursor)
                return render(request,'order/checkorder.html',{'list':row,'number':len(row)})
            if "Write Review" in y:
                return HttpResponseRedirect(reverse('makereview', args=(int(x),)))
        list = orders.objects.filter(userid=request.user.id,shipid=int(search['search']))
        cursor = connection.cursor()
        query = """SELECT order_orders.shipid, order_orders.status,
                               order_orders.addressx, order_orders.addressy, cart_carts.productid, cart_carts.count
                                from order_orders INNER JOIN cart_carts on cart_carts.ship_id = order_orders.shipid
                               WHERE order_orders.userid = %s AND cart_carts.ship_id = %s"""
        cursor.execute(query, (str(request.user.id), str(search['search'])))
        row = dictfetchall(cursor)
        return render(request, 'order/checkorder.html', {'list': row, 'number': len(row)})
       # myreview = request.POST.dict()
       # print(request.POST)
       # for (x, y) in myreview.items():
       #     if 'Write Review' in y:
       #         return HttpResponseRedirect(reverse('makereview', args=(int(x),)))
       # return render(request, 'order/checkorder.html', {'number': 0})

def mailsend(userid):
    #write your sql
    username = userid.username
    receiver = []
    receiver.append(userid.email)
    subject = username+ ': Your Recent Order Update'
    message = 'Hi ' + userid.username + ' your package has been delivered. Go to your order history make some comments and earn rewards!'
    send_mail(subject, message, settings.EMAIL_HOST_USER, receiver, )