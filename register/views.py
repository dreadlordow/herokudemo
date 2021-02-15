from django.contrib.auth import login
from django.shortcuts import render, redirect

from register.forms import RegisterForm, ProfilePictureForm


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        profile_picture_form = ProfilePictureForm()
        context={
            'form': form,
            'profile_picture_form': profile_picture_form,
        }
        return render(request, 'register/register.html', context)
    else:
        form = RegisterForm(request.POST)
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid() and profile_picture_form.is_valid():
            user = form.save()
            profile_picture = profile_picture_form.save(commit=False)
            profile_picture.user = user
            profile_picture.save()

            login(request, user)
            return redirect('/')

        context = {
            'form': form,
            'profile_picture_form': profile_picture_form,
        }
        return render(request, 'register/register.html', context)
