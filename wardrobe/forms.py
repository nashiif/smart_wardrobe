from django import forms
from .models import ClothingItem, Outfit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        fields = ['name', 'category', 'color', 'image']

class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ['name', 'items']



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)