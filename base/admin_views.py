from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateProductForm, CreateComponentForm, CreateCpsDetailsForm
from .models import Products

@login_required(login_url='login')
def admin(request):
    products = Products.objects.all()
    context = {'products': products}
    return render(request, 'base/admin.html', context)


@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else :
        form = CreateProductForm()
    context = {'form': form}
    return render(request, 'base/add_product.html', context)

@login_required(login_url='login')
def full_access_components(request):
    form_1 = CreateComponentForm()
    form_2 = CreateCpsDetailsForm()
    if request.method == 'POST':
        form_1 = CreateComponentForm(request.POST)
        form_2 = CreateCpsDetailsForm(request.POST)
        # Check if both forms are valid
        if form_1.is_valid():
            form_1.save()
            return redirect('access_components')
        
        if form_2.is_valid():
            form_2.save()
            return redirect('access_components')
    context = {'form_1': form_1, 'form_2': form_2}
    return render(request, 'base/full_access_components.html', context)