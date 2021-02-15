from django import forms
from django.contrib.auth.models import User
from django.forms import HiddenInput

from mainsite.models import Product, Cart, Order, Comment, ProductPicture


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('owner', 'views')


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'


class OrderForm(forms.ModelForm):
    telephone = forms.CharField(min_length=13, max_length=13, initial='+359')

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'telephone', 'address')
        exclude=('user', 'date', 'total_cost', 'total_products', )


class SortForm(forms.Form):
    choices = (
        ('date_added', 'Date Ascending'),
        ('-date_added', 'Date Descending'),
        ('price', 'Price Ascending'),
        ('-price', 'Price Descending'),
        ('product_name', 'Name A-Z'),
        ('-product_name', 'Name Z-A'),
        ('-views', 'Most Viewed'),
        ('views', 'Least Viewed'),
    )
    order = forms.ChoiceField(choices=choices)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('user', 'product')


class ProductPictureForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = ProductPicture
        fields = ('image', )


class ProductFilterForm(forms.Form):
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)
    city = forms.CharField(max_length=20)

