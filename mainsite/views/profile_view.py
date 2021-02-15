from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import UpdateView

from mainsite.models import ProfilePicture
from mainsite.views.categoryfn import category_fn


def profile(request, slug):
    if request.method == 'GET':
        owner = User.objects.get(username=slug)
        try:
            profile_picture_exists = owner.profilepicture
        except ProfilePicture.DoesNotExist:
            profile_picture_exists = ProfilePicture(profile_picture='profile_pics/default_profile_picture.png', user=owner)
        products = owner.product_set.all()
        categories = category_fn()
        context = {
            'products': products,
            'owner': owner,
            'categories': categories,
            'profile_picture_exists': profile_picture_exists,
        }
        return render(request, 'profile.html', context)


class ProfileUpdate(UpdateView):
    model = User
    fields = ('username','email', 'first_name', 'last_name')
    template_name = 'update_profile.html'