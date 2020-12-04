from jamup.models import Post, Reply, Profile, Message
from jamup.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView, OwnerDeleteViewMessage
from jamup.forms import CreateForm, ReplyForm, ProfileCreateForm, MessageCreateForm

from django.core.files.uploadedfile import InMemoryUploadedFile

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q

class PostListView(OwnerListView):
    model = Post
    template_name = "jamup/post_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            query = Q(title__contains=strval)
            query.add(Q(text__contains=strval), Q.OR)
            query.add(Q(city__name__contains=strval), Q.OR)
            query.add(Q(state__name__contains=strval), Q.OR)
            query.add(Q(reason__name__contains=strval), Q.OR)
            objects = Post.objects.filter(query).select_related().order_by('-updated_at')
        else :
            # try both versions with > 4 posts and watch the queries that happen
            objects = Post.objects.all().order_by('-updated_at')
            # objects = Post.objects.select_related().all().order_by('-updated_at')[:10]

        # Augment the post_list
        for obj in objects:
            obj.natural_updated = naturaltime(obj.updated_at)

        post_list = objects

        ctx = {'post_list' : post_list, 'search': strval}
        retval = render(request, self.template_name, ctx)

        return retval


class PostDetailView(OwnerDetailView):
    model = Post
    template_name = 'jamup/post_detail.html'

    def get(self, request, pk) :
        x = Post.objects.get(id=pk)
        replies = Reply.objects.filter(post=x).order_by('-updated_at')
        reply_form = ReplyForm()
        context = { 'post' : x, 'replies': replies, 'reply_form': reply_form }
        return render(request, self.template_name, context)


class PostCreateView(OwnerCreateView):
    model = Post
    fields = ['title', 'city', 'state', 'reason', 'text']

    template_name = 'jamup/post_form.html'
    success_url = reverse_lazy('jamup:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        prof = get_object_or_404(Profile, user=self.request.user)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        post = form.save(commit=False)
        post.owner = self.request.user
        post.profile = prof
        post.save()
        return redirect(self.success_url)


class PostUpdateView(OwnerUpdateView):
    model = Post
    fields = ['title', 'city', 'state', 'reason', 'text']

    template_name = 'jamup/post_form.html'
    success_url = reverse_lazy('jamup:all')

    def get(self, request, pk=None):
        post1 = get_object_or_404(Post, id=pk, owner=self.request.user)
        form = CreateForm(instance=post1)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        post1 = get_object_or_404(Post, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=post1)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        post1 = form.save(commit=False)
        post1.save()

        return redirect(self.success_url)


class PostDeleteView(OwnerDeleteView):
    model = Post

class ReplyCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        p = get_object_or_404(Post, id=pk)
        reply = Reply(text=request.POST['reply'], owner=request.user, post=p)
        reply.save()
        return redirect(reverse('jamup:post_detail', args=[pk]))

class ReplyDeleteView(OwnerDeleteView):
    model = Reply
    template_name = "jamup/reply_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        post1 = self.object.post
        return reverse('jamup:post_detail', args=[post1.id])

class ProfileListView(OwnerListView):
    model = Profile
    template_name = "jamup/profile_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            # objects = Profile.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            query = Q(name__contains=strval)
            query.add(Q(bio__contains=strval), Q.OR)
            query.add(Q(city__name__contains=strval), Q.OR)
            query.add(Q(state__name__contains=strval), Q.OR)
            query.add(Q(genres__contains=strval), Q.OR)
            query.add(Q(instruments__contains=strval), Q.OR)
            objects = Profile.objects.filter(query).select_related().order_by('-updated_at')
        else :
            # try both versions with > 4 posts and watch the queries that happen
            objects = Profile.objects.all().order_by('-updated_at')
            # objects = Post.objects.select_related().all().order_by('-updated_at')[:10]

        # Augment the post_list
        for obj in objects:
            obj.natural_updated = naturaltime(obj.updated_at)

        profile_list = objects

        ctx = {'profile_list' : profile_list, 'search': strval}
        retval = render(request, self.template_name, ctx)

        return retval

class ProfileDetailView(OwnerDetailView):
    model = Profile
    template_name = 'jamup/profile_detail.html'

    def get(self, request, pk) :
        x = Profile.objects.get(id=pk)
        posts = Post.objects.filter(profile=x).order_by('-updated_at')
        profile_form = ProfileCreateForm()
        context = { 'profile' : x, 'posts': posts, 'profile_form': profile_form }
        return render(request, self.template_name, context)


class ProfileCreateView(OwnerCreateView):
    model = Profile
    fields = ['name', 'picture', 'city', 'state', 'bio', 'text', 'genres', 'instruments']

    template_name = 'jamup/profile_form.html'
    success_url = reverse_lazy('jamup:all')

    def get(self, request, pk=None):
        form = ProfileCreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = ProfileCreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        return redirect(self.success_url)


class ProfileUpdateView(OwnerUpdateView):
    model = Profile
    fields = ['name', 'picture', 'city', 'state', 'bio', 'text', 'genres', 'instruments']

    template_name = 'jamup/profile_form.html'
    success_url = reverse_lazy('jamup:all')

    def get(self, request, pk):
        profile1 = get_object_or_404(Profile, id=pk, user=self.request.user)
        form = ProfileCreateForm(instance=profile1)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        profile1 = get_object_or_404(Profile, id=pk, user=self.request.user)
        form = ProfileCreateForm(request.POST, request.FILES or None, instance=profile1)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        profile1 = form.save(commit=False)
        profile1.save()

        return redirect(self.success_url)


class ProfileDeleteView(OwnerDeleteViewMessage):
    model = Profile

class MessageListView(OwnerListView):
    model = Message
    template_name = "jamup/message_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            query = Q(text__contains=strval)
            query.add(Q(sender__username__contains=strval), Q.OR)
            query.add(Q(recipient__username__contains=strval), Q.OR)
            objects = Message.objects.filter(query).select_related().order_by('-created_at')
        else :
            objects = Message.objects.all().order_by('-created_at')

        message_list = objects

        ctx = {'message_list' : message_list}
        retval = render(request, self.template_name, ctx)

        return retval

class MessageCreateView(OwnerCreateView):
    model = Message
    fields = ['recipient', 'text']

    template_name = 'jamup/message_form.html'
    success_url = reverse_lazy('jamup:all')

    def get(self, request, pk=None):
        form = MessageCreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = MessageCreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        message = form.save(commit=False)
        message.sender = self.request.user

        message.save()
        return redirect(self.success_url)

class MessageDeleteView(OwnerDeleteViewMessage):
    model = Message

def stream_file(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    response = HttpResponse()
    response['Content-Type'] = profile.content_type
    response['Content-Length'] = len(profile.picture)
    response.write(profile.picture)
    return response

