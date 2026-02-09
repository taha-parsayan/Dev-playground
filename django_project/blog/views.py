from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'Taha Parsayan',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Feb 6, 2026'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'Feb 7, 2026'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context) # Render the home.html template with posts context

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'}) # Render the about.html template