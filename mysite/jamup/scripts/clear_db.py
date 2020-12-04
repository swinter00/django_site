from jamup.models import Post, Reply

def run():

    Post.objects.all().delete()
    Reply.objects.all().delete()