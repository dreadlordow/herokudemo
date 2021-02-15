from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import ListView

from mainsite.models import Product
from mainsite.views.categoryfn import category_fn
from mainsite.forms import SortForm

# def search(request):
#     query = request.GET['q']
#     products = Product.objects.filter(
#         product_name__icontains=query) | Product.objects.filter(description__icontains=query)
#     categories = category_fn()
#
#     context = {
#         'query': query,
#         'matched': products,
#         'categories': categories,
#         'products': products,
#     }
#     return render(request, 'search.html', context)

def extract_filter_value(params):
    order = params['order'] if 'order' in params else '-date_added'
    return order


class SearchView(ListView):
    template_name = 'search.html'
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):

        query = self.request.GET.get('q')
        context = super().get_context_data(**kwargs)
        categories = category_fn()
        context['query'] = query
        context['categories'] = categories
        context['sort_form'] = SortForm()

        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        city = self.request.GET.get('city')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        order = extract_filter_value(self.request.GET)
        if not order:
            order = '-date_added'

        try:
            products = self.request.GET.get('products')
            object_list = products

        except MultiValueDictKeyError:
            object_list = Product.objects.all()

        if query:
            object_list = Product.objects.filter(
                product_name__icontains=query) | Product.objects.filter(description__icontains=query)

        if city:
            object_list = object_list.filter(city__icontains=city)

        if min_price:
            object_list = object_list.filter(price__gte=min_price)

        if max_price:
            object_list = object_list.filter(price__lte=max_price)

        return object_list.order_by(order)

