from django.shortcuts import render
from .models import comments
from .forms import Makecomments
from order.models import wareHouse
from .models import comments
# Create your views here.
def makereview(request,id = 2):
    form = Makecomments
    if request.method == 'GET':
        product = wareHouse.objects.get(productid=id)
        return render(request, 'review/makereview.html', context={'form': form, 'proname': product.productname})
    if request.method == 'POST':
        form = Makecomments(request.POST)
        if form.is_valid():
            product = wareHouse.objects.get(productid=id)
            Comform = form.save(commit=False)
            Comform.product = product
            Comform.save()
            return render(request, 'review/thankreview.html', )
        return render(request, 'review/makereview.html', context={'form': form})

def readreview(request,id = 2):
    if request.method == 'GET':
        review = comments.objects.filter(product_id=id)
        product = wareHouse.objects.get(productid=id)
        return render(request, 'review/readreview.html', context={'list': review,'proname': product.productname,'number':len(review)})
