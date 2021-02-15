from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from mainsite.forms import SortForm, CommentForm, ProductFilterForm
from mainsite.models import Product, Comment, ProductPicture
from mainsite.views.categoryfn import category_fn
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.http.response import HttpResponseNotFound

def extract_filter_value(params):
    order = params['order'] if 'order' in params else '-date_added'
    return order


# def index(request):
#     order = extract_filter_value(request.GET)
#     products = Product.objects.all().order_by(order)
#     form = SortForm()
#     categories = category_fn()
#     context = {
#         'products': products,
#         'categories': categories,
#         'form': form,
#         'sort_form' : SortForm(),
#     }
#     return render(request, 'index.html', context)


class IndexView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        print(self.request.GET)
        self.products = Product.objects.all()
        self.order = extract_filter_value(self.request.GET)


        self.products = self.products.order_by(self.order)
        self.images = ProductPicture.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = category_fn()
        context['products'] = self.products
        context['sort_form'] = SortForm()
        context['filter_form'] = ProductFilterForm()
        context['order'] = self.order

        page_number = self.request.GET.get('page')
        paginator = Paginator(self.products, 8)

        context['paginator'] = paginator
        context['page_obj'] = paginator.get_page(page_number)
        context['is_paginated'] = True

        return context




def product(request, pk, slug=None):
    product = Product.objects.get(pk=pk)
    if request.method == 'GET':
        if slug is None:
            slug = product.product_name

        if slug and product.product_name.lower() != slug.lower():
            return HttpResponseNotFound('Product not found')

        product.views +=1
        product.save(update_fields=['views'])

        comment_form = CommentForm()
        product_comments = [c for c in Comment.objects.filter(product_id=pk)]
        owner = User.objects.get(pk=product.owner_id)
        context={
            'product': product,
            'owner': owner,
            'comment_form': comment_form,
            'product_comments': product_comments,
            'categories': category_fn(),
            'views': product.views,
        }
        return render(request, 'single_product.html', context)

    else:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            product_comments = [c for c in Comment.objects.filter(product_id=pk)]
            owner = User.objects.get(pk=product.owner_id)
            context = {
                'product': product,
                'owner': owner,
                'comment_form': CommentForm(),
                'product_comments': product_comments,
                'categories': category_fn(),
            }
            return render(request, 'single_product.html', context)
