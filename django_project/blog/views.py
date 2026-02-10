from django.shortcuts import render
from django.http import HttpResponse
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context) # Render the home.html template with posts context

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'}) # Render the about.html template