from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from mainsite.forms import ProductForm, ProductPictureForm
from mainsite.models import Product, ProductPicture
from mainsite.views.categoryfn import category_fn


def edit(request, pk):
    ImageFormSet = inlineformset_factory(Product, ProductPicture,fields=('images', ), extra=4)

    product = Product.objects.get(pk=pk)
    categories = category_fn()
    id = request.user.id

    if request.method == 'GET':
        form = ProductForm(instance=product)
        formset = ImageFormSet(instance=product)
        print(formset.queryset)
        context = {
            'form': form,
            'categories': categories,
            'product': product,
            'id': id,
            'formset': formset,

        }
        return render(request, 'edit_product.html', context)

    else:
        form = ProductForm(request.POST, instance=product)
        formset = ImageFormSet(request.POST, request.FILES, instance=product)

        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)  # Setting foreign key
            product.save()
            formset.save()

            return redirect('index')

        form = ProductForm(instance=product)
        context = {
            'form': form,
            'formset': ImageFormSet(instance=product),
            'categories':categories,
        }
        return render(request, 'create_product.html', context)