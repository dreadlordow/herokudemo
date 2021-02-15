from django.shortcuts import render

from mainsite.forms import SortForm
from mainsite.models import Product
from mainsite.views.categoryfn import category_fn
from django.core.paginator import Paginator


def extract_filter_value(params):
    order = params['order'] if 'order' in params else '-date_added'
    return order


def category_view(request, category):
    category = category
    categories = category_fn()
    if request.method == 'GET':
        #products = Product.objects.filter(category=category)

        sort_form = SortForm()
        order = extract_filter_value(request.GET)

        products = Product.objects.filter(category=category).order_by(order)

        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        context = {
            'category': category,
            'products': products,
            'categories': categories,
            'len': len(products),
            'page_obj': page_obj,
            'sort_form': sort_form,
            'order': order,
        }
        return render(request, 'category.html', context)


def search_in_category(request, category):
    category = category
    categories = category_fn()

    query = request.GET['q']
    sort_form = SortForm()
    order = extract_filter_value(request.GET)
    products = Product.objects.filter(category=category).filter(product_name__icontains=query).order_by(order)

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'len': len(products),
        'page_obj': page_obj,
        'query': query,
        'sort_form': SortForm(),
        'order': order,
    }
    return render(request, 'category.html', context)