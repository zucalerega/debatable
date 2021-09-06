from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from posts.models import Post, Like
from users.models import Profile
from users.models import Follow

def home_view(request):
    if request.user != 'AnonymousUser':
        queryset = []
        for i in Follow.objects.filter(follower = request.user):
            for j in Post.objects.filter(author = i.following):
                queryset.append([j, (len(Like.objects.filter(post=j, action=True))- len(Like.objects.filter(post=j, action=False)))])

        context = {"basic_suggestions": queryset}
    return render(request, 'users/home.html', context)

def search_view(request, username=''):
    query = request.POST.get('search', request.user)
    if User.objects.filter(username=query):
        return redirect("/profile/" + query + "/")
    return redirect('chat:chathome')

def construction_view(request):
    return render(request, 'construction.html')
