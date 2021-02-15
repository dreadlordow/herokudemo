from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from mainsite.forms import ProductForm, ProductPictureForm
from mainsite.models import ProductPicture
from mainsite.views.categoryfn import category_fn


@login_required(login_url='login')
def create_product(request):
    ImageFormSet = modelformset_factory(ProductPicture, form=ProductPictureForm, extra=4)

    categories = category_fn()
    if request.method == 'GET':
        form = ProductForm()
        formset = ImageFormSet(queryset=ProductPicture.objects.none())
        context = {
            'form': form,
            'formset': formset,
            'categories': categories,
        }
        return render(request, 'create_product.html', context)
    else:
        user = request.user
        form = ProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProductPicture.objects.none())

        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False) # Setting foreign key
            product.owner = user
            product.save()

            for f in formset.cleaned_data:
                if f:
                    image = f['image']
                    photo = ProductPicture(product=product, images=image)
                    photo.save()
            return redirect('index')

        form = ProductForm()
        context = {
            'form': form,
            'formset': formset,
            'categories':categories,
        }
        return render(request, 'create_product.html', context)