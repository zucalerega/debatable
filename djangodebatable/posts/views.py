from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Like
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from users.models import Follow

# Create your views here.

def feed_view(request):
    basic_suggestions = []
    for i in Follow.objects.filter(follower = request.user):
        for j in Post.objects.filter(author = i.following):
            basic_suggestions.insert(0, [j, (len(Like.objects.filter(post=j, action=True))- len(Like.objects.filter(post=j, action=False)))])
    context = {"basic_suggestions": basic_suggestions}

    return render(request, "posts/feed.html", context)

class PostListView(ListView):
    model=Post
    template_name='debatablePages/debatableHome.html'
    context_object_name='posts'
    ordering=['-date_posted']
    #posts per page
    paginate_by=2


class UserPostListView(ListView):
    model=Post
    template_name='posts/user_posts.html'
    context_object_name='posts'
    #posts per page
    paginate_by=5

    def get_queryset(self):
        user=get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(LoginRequiredMixin, DetailView):
    model=Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model=Post
    fields=['title', 'content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Post
    fields=['title', 'content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

def like_view(request, username="null"):
    if len(Like.objects.filter(actor=request.user, post=Post.objects.get(id=request.POST['post-title']), action=request.POST['action'])) == 0:
        like = Like.objects.create(actor=request.user, post=Post.objects.get(id=request.POST['post-title']), action=request.POST['action'])
    else:
        Like.objects.get(actor=request.user, post=Post.objects.get(id=request.POST['post-title']), action=request.POST['action']).delete()
    return redirect(request.META['HTTP_REFERER'])
