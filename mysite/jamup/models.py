from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings

class Post(models.Model):
        title = models.CharField(max_length=200)
        city = models.ForeignKey(City, on_delete=models.CASCADE)
        state = models.ForeignKey(State, on_delete=models.CASCADE)
        reason = models.ForeignKey(Reason, on_delete=models.CASCADE)
        text = models.TextField()
        owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        # Reply
        replies = models.ManyToManyField(settings.AUTH_USER_MODEL,
                through='Reply', related_name='replies_owned')

        # Shows up in the admin list
        def __str__(self):
                return self.title


class Reply(models.Model):
        text = models.TextField()

        post = models.ForeignKey(Post, on_delete=models.CASCADE)
        owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        # Shows up in the admin list
        def __str__(self):
                if len(self.text) < 15 : return self.text
                return self.text[:11] + ' ...'


class Profile(models.Model):
        name = models.CharField(max_length=50)
        city = models.ForeignKey(City, on_delete=models.CASCADE)
        state = models.ForeignKey(State, on_delete=models.CASCADE)
        bio = models.TextField(max_length=1000)
        owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        # Profile Picture
        picture = models.BinaryField(null=True, editable=True)
        content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

        # Posts
        posts = models.OneToManyField(settings.AUTH_USER_MODEL,
                through='Post', related_name='posts_owned')

        # Genres
        genres = models.ManyToManyField(settings.AUTH_USER_MODEL,
                through='Genre', related_name='genres_played')

        # Instruments
        instruments = models.ManyToManyField(settings.AUTH_USER_MODEL,
                through='Instrument', related_name='instruments_played')

        # Shows up in the admin list
        def __str__(self):
                return self.name

class State(models.Model):
        name = models.CharField(max_length=2)

        def __str__(self):
                return self.name

class City(models.Model):
        name = models.CharField(max_length=80)

        def __str__(self):
                return self.name

class Genre(models.Model):
        name = models.CharField(max_length=80)

        def __str__(self):
                return self.name

class Instrument(models.Model):
        name = models.CharField(max_length=80)

        def __str__(self):
                return self.name

class Reason(models.Model):
        name = models.CharField(max_length=80)

        def __str__(self):
                return self.name
