from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateProductForm, CreateComponentForm, CreateCpsDetailsForm
from base.models import Products, Components, Cps_details, Order
from django.shortcuts import get_object_or_404

@login_required
def admin_cards(request):
    orders = Order.objects.all()
    pending_orders = orders.filter(status='Pending')
    context = {'orders': orders, 'pending_orders': pending_orders}
    return render(request, 'admin/admin_cards.html', context)

@login_required
def admin_orders(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'admin/admin_orders.html', context)

@login_required
def admin_products(request):
    products = Products.objects.all()
    context = {'products': products}
    return render(request, 'admin/admin_products.html', context)

@login_required(login_url='login')
def admin(request):
    products = Products.objects.all()
    orders = Order.objects.all()
    pending_orders = orders.filter(status='Pending')
    context = {'products': products, 'orders': orders, 'pending_orders': pending_orders}
    return render(request, 'admin/admin.html', context)

# ! ----------- PRODUCTS ----------- ! #
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
    return render(request, 'admin/add_product.html', context)


@login_required(login_url='login')
def edit_product(request, pk):
    product = get_object_or_404(Products, id=pk)
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = CreateProductForm(instance=product)
    context = {'form': form, 'product': product}
    return render(request, 'admin/add_product.html', context)

def delete_product(request, pk):
    product = get_object_or_404(Products, id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin')
    context = {'product': product}
    return render(request, 'admin/delete.html', context)


# ! ----------- COMPONENTS ----------- ! #
@login_required(login_url='login')
def full_access_components_shapes(request):
    components = Components.objects.all()
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
    context = {'form_1': form_1, 'form_2': form_2, 'components': components}
    return render(request, 'admin/full_access_components.html', context)


@login_required(login_url='login')
def components_shapes(request):
    components = Components.objects.all()
    shapes = Cps_details.objects.all()
    context = {'components': components, 'shapes': shapes}
    return render(request, 'admin/components&shapes.html', context)


@login_required(login_url='login')
def edit_component(request, pk):
    component = get_object_or_404(Components, id=pk)
    if request.method == 'POST':
        form = CreateComponentForm(request.POST, instance=component)
        if form.is_valid():
            form.save()
            return redirect('components_shapes')
    else:
        form = CreateComponentForm(instance=component)
    context = {'form': form, 'component': component}
    return render(request, 'admin/edit_component.html', context)


@login_required(login_url='login')
def edit_shape(request, pk):
    shape = get_object_or_404(Cps_details, id=pk)
    if request.method == 'POST':
        form = CreateCpsDetailsForm(request.POST, instance=shape)
        if form.is_valid():
            form.save()
            return redirect('components_shapes')
    else:
        form = CreateCpsDetailsForm(instance=shape)
    context = {'form': form, 'shape': shape}
    return render(request, 'admin/edit_shape.html', context)