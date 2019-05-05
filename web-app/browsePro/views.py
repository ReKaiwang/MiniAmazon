from django.shortcuts import render
from cart.models import carts
from order.models import wareHouse
from .forms import Addcarts
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
# Create your views here.

def homepage(request):
    print(request.user.id)
    return render(request,'homepage.html',{})

def browsePro(request):
    form = Addcarts
    if request.method == 'POST':
        form = Addcarts(request.POST)
        if form.is_valid():
            #print(form['productId'])
            Comform = form.save(commit=False)
            myprevcart = carts.objects.filter(userid=request.user.id, status = 'InOrder')
            if(len(myprevcart.filter(productid = Comform.productid)) != 0):
                count = myprevcart.filter(productid = Comform.productid).get()
                count.count += Comform.count
                count.save()
            else:
                Comform.userid = request.user.id
                Comform.save()
            return HttpResponseRedirect('success/')
        else:
            print("wrong form")
    else:
        return render(request,'browsePro/browsePro.html',context = {'form':form})

def resultsView(request):
    #template_name = 'browsePro/addcartsuccess.html'
    return render(request, 'browsePro/addcartsuccess.html')

def showProList(request):
    if request.method == 'GET':
        #list = wareHouse.objects.all()
        return render(request,'browsePro/searchProduct.html',)
    if request.method == 'POST':
       # print(request.POST)
        search = request.POST.dict()
        print(search)
        for (x,y) in search.items():
            if "showlist" in x:
                list = wareHouse.objects.all()
                #print(len(list))
                return render(request, 'browsePro/showProductList.html', context={'list': list,'number':len(list)})
            if "See Review" in y:
                return HttpResponseRedirect(reverse('readreview', args=(int(x),)))
        list = wareHouse.objects.filter(productname__icontains= search['search'])
        return render(request, 'browsePro/showProductList.html', context={'list': list,'number':len(list)})
