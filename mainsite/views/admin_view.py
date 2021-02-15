from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render

from mainsite.models import Product, Order



@user_passes_test(lambda x: x.is_superuser or x.is_staff)
def admin_view(request):
    users = User.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()
    context ={
        'users': users,
        'products': products,
        'orders': orders,
    }

    return render(request, 'admin_page.html', context)