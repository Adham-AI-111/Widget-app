from django.shortcuts import render, redirect
from .models import Order, OrderImages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm, GetOrderForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .services.pagination import paginate_queryset

def home(request):
    user = request.user
    if user.is_authenticated:
        orders = Order.objects.filter(user=user)
        # ! --------Cards-------- 
        completed_orders = orders.filter(status__iexact='Completed')
        pending_orders = orders.filter(status__iexact='Pending')
        # --------- store the remaining balance for all orders------
        total_remaining_balance = []
        for order in orders:
            #? get remaining balance for each order
            total_remaining_balance.append(order.remaining_balance)
        
        # summarize the values to get the total
        total_remaining_balance = sum(total_remaining_balance)
        # -----------------------------------------------------------
        already_paid = 0
        for order in orders:
            already_paid += order.paid
        # !---------------------
        total_price = Order.get_total_user_order_price(user=user)
    else:
        return redirect('login')
    
    context = {
        'orders':orders,
        'completed_orders': completed_orders,
        'pending_orders':pending_orders,
        'total_remaining_balance':total_remaining_balance,
        'already_paid':already_paid,
        'total_price':total_price
        }
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def profile(request):
    user = request.user
    context = {'user':user}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def edit_profile(request):
    user =request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'profile updated successfully!!')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user)
    context = {'form':form}
    return render(request, 'base/edit_profile.html', context)


@login_required(login_url='login')
def user_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    # ! -------filter-------
    status_filter = request.GET.get('status_filter', '')
    date_filter = request.GET.get('date_filter', '')
    filters = {}
    if status_filter:
        filters['status__iexact'] = status_filter
    if date_filter:
        filters['due_date'] = date_filter

    # this variable that the rest view will 
    orders = orders.filter(**filters).distinct()

    # pagination
    page_obj, page_orders, qs_prefix = paginate_queryset(request, orders, per_page=10)
    # !----------------------

    context = {'user': user, 'orders': page_orders, 'page_obj': page_obj, 'qs_prefix': qs_prefix}
    return render(request, 'base/orders.html', context)


# !====== Get Order =========
@login_required(login_url='login')
def get_order(request):
    user = request.user
    if request.method == 'POST':
        form = GetOrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = user
            order.save()
            messages.success(request, 'order details was saved now share images if you want')
            return redirect('upload_images', order_id=order.id)
    else:
        form = GetOrderForm()
    context = {'form':form}
    return render(request, 'base/request_order.html', context)


# !=========>
# views.py (same as before)
def upload_order_images(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        images = request.FILES.getlist('images')  # Gets files from HTML input
        
        # Manual validation
        errors = []
        if not images:
            errors.append("Please select at least one image")
        elif len(images) > 6:
            errors.append("Maximum 6 images allowed")
        
        for image in images:
            if image.size > 3 * 1024 * 1024:
                errors.append(f"File {image.name} is too large (max 3MB)")
            if not image.content_type.startswith('image/'):
                errors.append(f"{image.name} is not a valid image file")
        
        if not errors:
            for image in images:
                OrderImages.objects.create(order=order, image=image)
            
            order.save()
            
            messages.success(request, f"Successfully uploaded {len(images)} images, and the order was submited (price and status in order management)")
            return redirect('user_orders')
        else:
            for error in errors:
                messages.error(request, error)
    
    return render(request, 'base/upload_images.html', {'order': order})
#! ===========>

@login_required(login_url='login')
def user_edit_order(request, pk):
    user = request.user
    order = get_object_or_404(Order, id=pk)
    # prevent user from access if status of order is 'in progress'
    if order.status != 'Pending':
        messages.info(request, 'you cannot update the order while processing or delivering (contact with admin if wanted)')
        return redirect('user_orders')
    
    if request.method =='POST':
        form = GetOrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = user
            order.save()
            messages.success(request, 'order was updated')
            return redirect('user_orders')
    else:
        form = GetOrderForm(instance=order)
    context = {'form':form}
    return render(request, 'base/user_edit_order.html', context)