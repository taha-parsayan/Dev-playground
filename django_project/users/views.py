from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages # message.debug, message.info, message.success, message.warning, message.error
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  # instantiate the form with POST data
        if form.is_valid():
            form.save()  # Save the form to create the user
            username = form.cleaned_data.get('username')  # Get the username from the cleaned data
            messages.success(request, f'Account created for {username}!')  # Add a success message to be displayed to the user
            return redirect('users-login')  # Redirect to the login page after successful registration
            # the -home is added by django
        
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')  # Add an error message if the form is not valid
    else:
        form = UserRegisterForm()  # instantiate the UserRegisterForm
    return render(request, 'users/register.html', {'form': form})  # Correct template path as a string



@login_required # Decorator to ensure that only logged-in users can access the profile view
def profile(request):
    return render(request, 'users/profile.html')  # Correct template path as a string