from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Product(models.Model):
    cat = (
        ('Electronic', 'Electronic'),
        ('Clothing', 'Clothing'),
        ('Automobiles', 'Automobiles'),
        ('Sport', 'Sport'),
        ('Books', 'Books'),
        ('Services', 'Services'),
        ('Other', 'Other'),

    )
    product_name = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=600, blank=False)
    category = models.CharField(max_length=30, choices=cat, blank=False)
    price = models.FloatField(blank=False)
    city = models.CharField(max_length=30, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.product_name} - {self.price} - listed by: {self.owner}'


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        cart = Cart.objects.get(user=self.user)
        return f'{self.user.username}\'s shopping cart with {cart.products.all().count()} items'


class Order(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=False)
    telephone = models.CharField(max_length=13, blank=False, default='+359')
    address = models.CharField(max_length=50, blank=False)
    user = models.ForeignKey(User, null=False, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    total_cost = models.IntegerField(default=0)
    total_products = models.IntegerField(default=0)


    def __str__(self):
        return f'Order id {self.id}, made by {self.user.username} on {self.date}'


class ProfilePicture(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ProductPicture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='product_pictures/',blank=False,verbose_name='Image')


