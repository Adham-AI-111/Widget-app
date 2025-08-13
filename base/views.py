from django.shortcuts import render, redirect
from .models import User, Order
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Products
from .forms import OrderForm
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'base/home.html')


@login_required(login_url='login')  
def profile(request):
    user = request.user

    context = {'user': user}
    return render(request, 'base/profile.html', context)


def gallery(request):
    products = Products.objects.all()
    context = {'products': products}
    return render(request, 'base/gallery.html', context)


@login_required(login_url='login')
def get_product(request, pk):
    product = Products.objects.get(id=pk)
    if not product:
        messages.error(request, "Product not found.")
        return redirect('gallery')
    
    if request.method == 'POST':
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "You must be logged in to request a product.")
            return redirect('login')
        
        # create order form to get product
        form = OrderForm(request.POST, product=product)    
        if form.is_valid():
            order = form.save(commit=False)  
            order.user = user
            order.product = product
            order.save()
            messages.success(request, "Product requested successfully.")
        return redirect('gallery')
    else:
        form = OrderForm(product=product)

    context = {'form':form, 'product':product}
    return render(request, 'base/get_product.html', context)