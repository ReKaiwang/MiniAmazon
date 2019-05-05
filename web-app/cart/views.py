from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from browsePro.forms import Addcarts
from order.models import orders
from order.forms import myorders
from .forms import Addorders
from .webrequest import WebRequest
from .models import carts
from order.models import wareHouse
# Create your views here.
HOST = 'amazonproxy'
PORT = 55555
addr = (HOST, PORT)
def delteitem(id):
    list = carts.objects.get(id=id)
    list.delete()
def editcart(id,count):
    list = carts.objects.get(id=id)
    list.count = count
    list.save()
def viewcarts(request):
    if request.method == 'GET':
        list = carts.objects.filter(userid=request.user.id,status = "InOrder")
        number = len(list)
        print(number)
        return render(request,'carts/viewcarts.html',context ={'list':list, 'number':number})
        #return render_to_response("carts/viewcarts.html", locals())
    if request.method == 'POST':
        myupdate = request.POST.dict()
        for (x,y) in myupdate.items():
            if "Delete" in y:
                delteitem(int(x))
            if "Edit" in y:
                mylist = request.POST.getlist(x)
                if mylist[0] == '0':
                    delteitem(int(x))
                else:
                    editcart(int(x),int(mylist[0]))
        list = carts.objects.filter(userid=request.user.id,status = "InOrder")
        number = len(list)
        return render(request, 'carts/viewcarts.html', context={'list': list,'number':number})
def checkout(request):
   # form = Addorders
    form = myorders
    if request.method == 'POST':
        form = myorders(request.POST)
        if form.is_valid():
            Comform = form.save(commit=False)
            Comform.userid = request.user.id
            print("my user id is %s" % str(request.user.id))
            Comform.status = "InWareHouse"
            list = carts.objects.filter(userid=request.user.id, status = "InOrder")
            Comform.save()
            wp = WebRequest(addr, 1, Comform.addressx, Comform.addressy, Comform.shipid, Comform.upsid)
            for x in list:
                x.status = "InHouse"
                x.ship = Comform
                x.save()
                descri = wareHouse.objects.get(productid=x.productid).description
                wp.add_products(str(x.productid),str(descri),x.count)
            print(wp.acommunicate)
            wp.send_request()
        return render(request, 'carts/checkoutresult.html', context={'shipid': Comform.shipid})
    return render(request, 'carts/checkout.html', context={'form': form})
