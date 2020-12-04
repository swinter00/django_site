from django.contrib import admin
from jamup.models import State, City, Reason, Post, Reply, Profile

# Register your models here.

admin.site.register(State)
admin.site.register(City)
admin.site.register(Reason)
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(Profile)