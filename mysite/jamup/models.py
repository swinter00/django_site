from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class State(models.Model):
        name = models.CharField(max_length=20)

        def __str__(self):
                return self.name

class City(models.Model):
        name = models.CharField(max_length=80)
        state = models.ForeignKey(State, on_delete=models.CASCADE)

        def __str__(self):
                return self.name

class Reason(models.Model):
        name = models.CharField(max_length=80)

        def __str__(self):
                return self.name

class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
        name = models.CharField(max_length=50)
        city = models.ForeignKey(City, on_delete=models.CASCADE)
        state = models.ForeignKey(State, on_delete=models.CASCADE)
        bio = models.TextField(max_length=1000)
        private = models.BooleanField(default=False)

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        # Profile Picture
        picture = models.BinaryField(null=True, editable=True, default=False)
        content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file', default='')

        # Genres
        genres = models.TextField(max_length=300)

        # Instruments
        instruments = models.TextField(max_length=300)

        # Shows up in the admin list
        def __str__(self):
                return self.name

class Post(models.Model):
        title = models.CharField(max_length=200)
        city = models.ForeignKey(City, on_delete=models.CASCADE)
        state = models.ForeignKey(State, on_delete=models.CASCADE)
        reason = models.ForeignKey(Reason, on_delete=models.CASCADE)
        text = models.TextField()
        profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
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

class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
