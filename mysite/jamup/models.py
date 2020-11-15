from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings

class Post(models.Model):
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    city = models.CharField(
            max_length=80,
            validators=[MinLengthValidator(2, "City must be greater than 2 characters")]
    )
    state = models.CharField(
            max_length=2,
    )
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Comment
    replies = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Reply', related_name='replies_owned')

    # Shows up in the admin list
    def __str__(self):
        return self.title


class Reply(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(3, "Reply must be greater than 3 characters")]
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'


class UserInfo(models.Model):
    name = models.CharField(
            max_length=30,
            validators=[MinLengthValidator(2, "Name must be greater than 2 characters")]
    )
    city = models.CharField(
            max_length=80,
            validators=[MinLengthValidator(2, "City must be greater than 2 characters")]
    )
    state = models.CharField(
            max_length=2,
    )
    bio = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    instruments = models.TextField()
    genres = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Picture
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

    # Posts
    posts = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Post', related_name='posts_owned')

    # Shows up in the admin list
    def __str__(self):
        return self.name