from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # import User model for author field

class Post(models.Model):
    title = models.CharField(max_length=100) # character field with max length 100
    content = models.TextField() # text field for long text
    date_posted = models.DateTimeField(default=timezone.now) # date and time field with default value as current time
    author = models.ForeignKey(User, on_delete=models.CASCADE) # foreign key to User model


    # This method is used to return a string representation of the Post object.
    def __str__(self):
        return self.title
    

'''
After defining models in blog/models.py, follow these steps to set up the database:
    1. Add "blog.apps.BlogConfig" to the INSTALLED_APPS list in mysite/settings.py.
    2. Run python manage.py makemigrations to create migration files for the blog app.
    3. Run python manage.py sqlmigrate blog 0001 to see the SQL statements for the first migration of the blog app.
    4. Run python manage.py migrate to apply the migrations and create the necessary tables in the database.
    5. (Optional) Run python manage.py shell to interact with the database and test your models.
       A better option is to use the DB Browser for SQLite app to view and manage the database.

    In shell:
    from blog.models import Post
    from django.contrib.auth.models import User

    User.objects.all() # get all users from the database
    User.objects.filter(username='taha') # filter users by username
    User.objects.get(username='taha') # get a single user by username

    user = User.objects.first() # get the first user from the database

    user.id # get the primary key of the user
    user.pk # pk is an alias for id, so it will return the same value as user.id

    post = Post(title='My First Post', content='This is the content of my first post.', author=user) # create a new Post instance
    post.save() # save the Post instance to the database

    post_1 = Post(title='Weather', content='Denmark is cold!', author=user)
    post_1.save() # save the Post instance to the database

    user.post_set.all() # get all posts related to the user using the reverse relationship
    # the _set is added by Django to access related objects.

    user.post_set.create(title = 'PhD',content='Research is time-consuming') # create a new Post instance related to the user and save it to the database in one step
'''