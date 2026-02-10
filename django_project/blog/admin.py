from django.contrib import admin
from .models import Post # import the Post model from the current app's models.py file

admin.site.register(Post) # register the Post model with the admin site to make it accessible in the admin interface