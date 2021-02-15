from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.core.exceptions import ValidationError

from mainsite.models import ProfilePicture


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already taken!')
        return self.cleaned_data


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ProfilePicture
        exclude = ('user', )