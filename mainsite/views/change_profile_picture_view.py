from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from mainsite.models import ProfilePicture
from register.forms import ProfilePictureForm


def change_profile_picture(request,slug=None, pk=None):
    user = User.objects.get(pk=pk)
    if request.method == 'GET':
        if request.user.id == pk:
            context ={
                'form': ProfilePictureForm(),
                'pfp': ProfilePicture.objects.get(user_id=user.id),
            }

            return render(request, 'change_pfp.html', context)
        return redirect('index')

    else:
        form = ProfilePictureForm(request.POST, request.FILES)
        if request.FILES:
            if form.is_valid():
                picture = form.save(commit=False)
                if ProfilePicture.objects.filter(user_id=pk).count():
                    ProfilePicture.objects.get(user_id=pk).delete()
                picture.user_id = user.id
                picture.save()
                context={
                    'owner': user,
                    'products': user.product_set.all(),


                }
                return redirect('profile', user.username)
            return render(request, 'change_pfp.html', {'form': form})

        # If there is no new profile picture selected
        context = {
            'form': ProfilePictureForm(),
            'pfp': ProfilePicture.objects.get(user_id=user.id),
        }

        return render(request, 'change_pfp.html', context)
