from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from mainsite.forms import OrderForm
from mainsite.models import Cart
from mainsite.views.categoryfn import category_fn


def checkout(request):
    if request.method == 'GET':
        form = OrderForm()
        form.fields['email'].initial = User.objects.get(pk=request.user.id).email
        categories = category_fn()
        context = {
            'form': form,
            'categories': categories,
        }
        return render(request, 'checkout.html', context)


def order(request, pk):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        user = User.objects.get(pk=pk)
        cart = Cart.objects.get(user=user)
        products = cart.products.all()
        cost = sum(products.values_list('price', flat=True))
        print(cost)
        context = {
            'products': products,
            'len': len(products),
            'cost': cost,
        }
        if form.is_valid():
            new = form.save(commit=False) # Setting foreign key
            new.user = user
            new.total_cost = cost
            new.total_products = len(products)
            new.save()
            cart.products.clear()
            return render(request, 'order_complete.html', context)
        context = {
            'form': form,
        }
        return render(request, 'checkout.html', context)