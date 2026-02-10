'''
Purpose: This file defines a custom user registration form by inheriting from Django's built-in UserCreationForm. 
It adds an email field to the form and specifies the fields to be included in the form through the Meta class.
'''

from django import forms
from django.contrib.auth.forms import UserCreationForm # to create a custom user registration form
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm): # inherit from UserCreationForm to create a custom registration form
    email = forms.EmailField()

    class Meta:
        # specify the model to be used for the form, which is the built-in User model
        model = User 
        # specify the fields to be included in the form, which are username, email, password1, and password2 (password confirmation)
        fields = ['username', 'email', 'password1', 'password2']