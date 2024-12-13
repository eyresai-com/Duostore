from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Cart
from .forms import orderStatusForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from vendor.models import Vendor

# Admin All Orders
@login_required(login_url='login')
def adminAllOrders(request):
    try:
        vendor = Vendor.objects.get(user=request.user)  # Fetch vendor instance
    except Vendor.DoesNotExist:
        messages.error(request, "No vendor associated with this user.")
        return redirect('some_fallback_url')    
    
    orders = Order.objects.filter(is_ordered=True, vendor=vendor).order_by('-ordered_at')
    pending_orders = orders.filter(status='pending').count()
    confirmed_orders = orders.filter(status='confirmed').count()
    canceled_orders = orders.filter(status='canceled').count()

    context = {
        'title': 'All Orders',
        'orders': orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'canceled_orders': canceled_orders,
    }
    
    return render(request, 'orders/orders.html', context)

# Admin Order Delete
@login_required(login_url='login')
def adminOrderDelete(request, order_id):
    vendor = request.user.vendor
    order = get_object_or_404(Order, order_id=order_id, vendor=vendor)
    order.delete()
    messages.success(request, 'Order deleted successfully!')
    return redirect('adminAllOrders')

# Admin Pending Orders
@login_required(login_url='login')
def adminPendingOrders(request):
    vendor = request.user.vendor
    orders = Order.objects.filter(status='pending', is_ordered=True, vendor=vendor).order_by('-ordered_at')

    context = {
        'title': 'Pending Orders',
        'orders': orders
    }
    
    return render(request, 'orders/pending-orders.html', context)

# Admin Confirmed Orders
@login_required(login_url='login')
def adminConfirmedOrders(request):
    vendor = request.user.vendor
    orders = Order.objects.filter(status='confirmed', is_ordered=True, vendor=vendor).order_by('-ordered_at')

    context = {
        'title': 'Confirmed Orders',
        'orders': orders
    }
    
    return render(request, 'orders/confirmed-orders.html', context)

# Admin Completed Orders
@login_required(login_url='login')
def adminCompletedOrders(request):
    vendor = request.user.vendor
    orders = Order.objects.filter(status='completed', is_ordered=True, vendor=vendor).order_by('-ordered_at')

    context = {
        'title': 'Completed Orders',
        'orders': orders
    }
    
    return render(request, 'orders/completed-orders.html', context)

# Admin Canceled Orders
@login_required(login_url='login')
def adminCanceledOrders(request):
    vendor = request.user.vendor
    orders = Order.objects.filter(status='canceled', is_ordered=True, vendor=vendor).order_by('-ordered_at')

    context = {
        'title': 'Canceled Orders',
        'orders': orders
    }
    
    return render(request, 'orders/canceled-orders.html', context)

# Admin Order Details
@login_required(login_url='login')
def adminOrderDetails(request, order_id):
    vendor = request.user.vendor
    order = get_object_or_404(Order, order_id=order_id, vendor=vendor, is_ordered=True)
    cart_items = Cart.objects.filter(order=order)

    if request.method == 'POST':
        form = orderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order status updated successfully!')
            return redirect('adminOrderDetails', order.order_id)
    else:
        form = orderStatusForm(instance=order)

    context = {
        'order': order,
        'cart_items': cart_items,
        'form': form,
    }
    
    return render(request, 'ecom/partials/order-details.html', context)



#------------------------------------------ Customer Side ------------------------------------------#