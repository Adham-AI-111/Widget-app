from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from custom_admin.forms import AdminOrderEditForm, AdminOrderCreationForm
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from base.models import Order
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.db.models import F
from base.services.pagination import paginate_queryset

# here is admin decorator
def admin_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'admin access required!!')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# ! ----------- ADMIN review ----------- ! #
@admin_required
def admin_cards(request):
    orders = Order.objects.all()
    today = timezone.now()
    #! orders status
    pending_orders = Order.objects.filter(status__iexact='Pending')
    orders_inprogress = Order.objects.filter(status__iexact='InProgress')
    completed_orders = Order.objects.filter(status__iexact='Completed')
    cancelled_orders = Order.objects.filter(status__iexact='Cancelled')
    deliverd_orders = Order.objects.filter(status__iexact='Deliverd')
    quick_orders = Order.objects.filter(is_quick=True)
    
    # orders filtered on dates
    today_orders = orders.filter(due_date=timezone.now().date())
    # ? order added since two dyas 
    two_days_ago = today - timedelta(days=2)
    new_orders_added = Order.objects.filter(created_at__gte=two_days_ago)

    # used dates for revenue
    _month = today.month
    _year = today.year

    #! Calculate monthly orders and revenue revenue
    monthly_orders = orders.filter(created_at__year=_year, created_at__month=_month)
    monthly_revenue = monthly_orders.aggregate(total=Sum('paid'))['total'] or 0

    #! total revenune
    # revenue = 0
    # for order in orders:
    #     revenue += order.paid
    revenue = Order.objects.aggregate(total=Sum('paid'))['total'] or 0

    #! calc the total remaining balance for all orders to display for the admin
    total_remaining_balance = []
    for order in orders:
        total_remaining_balance.append(order.remaining_balance)
    total_remaining_balance = sum(total_remaining_balance)

    #! number of delayed balance orders
    delayed_balance_orders = Order.get_delayed_order_balance().count()

    total_revenue = Order.get_total_revenue()

    context = {
        'orders': orders, 'pending_orders': pending_orders,
        'orders_inprogress':orders_inprogress, 'completed_orders':completed_orders,
        'deliverd_orders':deliverd_orders, 'quick_orders':quick_orders,
        'today_orders':today_orders, 'cancelled_orders':cancelled_orders, 'new_orders_added':new_orders_added,
        'total_remaining_balance':total_remaining_balance, 'revenue':revenue,
        'delayed_balance_orders':delayed_balance_orders, 'total_revenue':total_revenue,
        'monthly_orders':monthly_orders,'monthly_revenue':monthly_revenue,
            }
    return render(request, 'admin/admin_cards.html', context)

@admin_required
def admin_orders(request):
    orders = Order.objects.all()

    # Search functionality
    q = request.GET.get('q', '')
    q_search = Q()
    if q:
        q_search |= (
            Q(user__full_name__icontains=q)|
            Q(details__icontains=q)
        )

    status_filter = request.GET.get('status_filter', '')
    quick_filter = request.GET.get('quick_filter', '')
    date_filter = request.GET.get('date_filter', '')
    filters = {}
    if status_filter:
        filters['status__iexact'] = status_filter
    if quick_filter:
        if quick_filter == 'quick':
            filters['is_quick'] = True
        elif quick_filter == 'regular':
            filters['is_quick'] = False
    if date_filter:
        filters['created_at'] = date_filter

    orders = orders.filter(q_search, **filters).distinct()

    # pagination
    page_obj, page_orders, qs_prefix = paginate_queryset(request, orders, per_page=15)
    context = {'orders': page_orders, 'page_obj': page_obj, 'qs_prefix': qs_prefix}
    return render(request, 'admin/admin_orders.html', context)

@admin_required
def delayed_balance_orders(request):
    orders = Order.get_delayed_order_balance()

    # search 
    q = request.GET.get('q', '')
    q_search = Q()
    if q:
        q_search |= (
            Q(user__full_name__icontains=q)|
            Q(details__icontains=q)
        )
    orders = orders.filter(q_search).distinct()

    # pagination
    page_obj, page_orders, qs_prefix = paginate_queryset(request, orders, per_page=15)
    context = {'orders': page_orders, 'page_obj': page_obj, 'qs_prefix': qs_prefix}
    return render(request, 'admin/delayed_balance_orders.html', context)

@admin_required
def quick_orders(request):
    orders =  Order.objects.filter(is_quick=True)

    # search 
    q = request.GET.get('q', '')
    q_search = Q()
    if q:
        q_search |= (
            Q(user__full_name__icontains=q)|
            Q(details__icontains=q)
        )
    orders = orders.filter(q_search).distinct()

    # pagination
    page_obj, page_orders, qs_prefix = paginate_queryset(request, orders, per_page=15)
    context = {'orders': page_orders, 'page_obj': page_obj, 'qs_prefix': qs_prefix}
    return render(request, 'admin/quick_orders.html', context)

# ! ----------- PRODUCTS ----------- ! #

# ! ----------- COMPONENTS ----------- ! #

# ! ----------- ORDERS ----------- ! #
@admin_required
def edit_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        form = AdminOrderEditForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin_orders')
    else:
        form = AdminOrderEditForm(instance=order)
    context = {'form': form, 'order': order}
    return render(request, 'admin/edit_order.html', context)


@admin_required
def delete_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('admin_orders')
    context = {'order': order}
    return render(request, 'base/delete.html', context)

@admin_required
def add_order(request):
    user = request.user
    if request.method == 'POST':
        form = AdminOrderCreationForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = user
            order.save()
            messages.success(request, 'order added successfully')
            return redirect('admin_orders')
    else:
        form = AdminOrderCreationForm()
    context = {'form':form}
    return render(request, 'admin/add_order.html', context)
