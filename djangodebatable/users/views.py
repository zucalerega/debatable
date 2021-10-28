from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, ReportForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .models import Profile, Report, Follow, Feedback
from users import views as user_views
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, QuizForm, FeedbackForm
from django.contrib.auth.models import User
from posts.models import Post, Like
from django.urls import reverse
from chat.models import Rating
# Create your views here.
def stop_search(request):
    user = Profile.objects.get(user=request.user)
    user.searching = False
    user.save()


def home_view(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            Profile.objects.create(user=User.objects.get(username=username))
            return redirect("/profileChange/")
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form':form})

@login_required
def dynamic_lookup_view(request, username):
    stop_search(request)
    obj = get_object_or_404(Profile, user=User.objects.filter(username=username)[0])
    follow = len(Follow.objects.filter(follower=request.user, following=User.objects.get(username=username)))
    obj.respecting = len(Follow.objects.filter(follower=User.objects.get(username=username)))
    obj.respectedBy = len(Follow.objects.filter(following=User.objects.get(username=username)))
    obj.save()
    ratings = Rating.objects.filter(recipient=str(username))
    posts = []
    for j in Post.objects.filter(author = User.objects.filter(username=username)[0]):
        posts.append([j, (len(Like.objects.filter(post=j, action=True))- len(Like.objects.filter(post=j, action=False)))])
    like_list = []
    dislike_list = []

    for like in Like.objects.filter(actor=request.user):
        if like.action == True:
            like_list.append(like.post)
        else:
            dislike_list.append(like.post)

    econ_style = str(int(float(obj.ideology.split(",")[0]) * 5.6) - 83)+"px"
    auth_style = str(int(float(obj.ideology.split(",")[1]) * -5.6) + 5)+"px"
    context = {"like_list": like_list, "dislike_list": dislike_list, "object": obj, "follow": follow, "totalratings": len(Rating.objects.filter(recipient=str(username))), "ratings": ratings, "posts": posts, "auth_style": auth_style, "econ_style": econ_style}
    return render(request, "users/profile.html", context)

def profile_list_view(request):
	queryset = Profile.objects.all()
	context = {
		"object_list": queryset
	}
	return render(request, "users/profile.html", context)

@login_required
def profileChange(request):
    #stop_search(request)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Update success')
            return redirect('quiz')
    else:
        u_form=UserUpdateForm(instance = request.user)
        p_form=ProfileUpdateForm(instance = request.user.profile)
    context={
        'u_form':u_form,
        'p_form':p_form,

    }
    return render(request, 'users/profileChange.html', context)

@login_required
def report_view(request, username):
    obj = Report.objects.create(offender=username, reporter=request.user.username)
    form = ReportForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()

        form = ReportForm()
        messages.success(request, f'User Reported')

        return redirect('users:profile', username)
    context = {
    'form': form
    }

    return render(request, "users/report.html", context)

def follow_view(request, username):
    if len(Follow.objects.filter(follower=request.user, following=User.objects.get(username=username))) == 0:
        follow = Follow.objects.create(follower=request.user, following=User.objects.get(username=username))
    else:
        Follow.objects.get(follower=request.user, following=User.objects.get(username=username)).delete()
    return redirect('users:profile', username)

def quiz_view(request):
    stop_search(request)
    form = QuizForm(request.POST or None, instance = request.user)
    if form.is_valid():
        form.save()
        auth_num = 0
        econ_num = 0
        for item in form.cleaned_data:
            if '1_' in item or '2_' in item or '3_' in item or '4_' in item or '5_' in item:
                econ_num += form.cleaned_data[item]
            else:
                auth_num += form.cleaned_data[item]
        econ_num = econ_num/5 - 10
        auth_num = auth_num/5 - 10
        user = Profile.objects.get(user=request.user)
        user.ideology = str(round(float(econ_num), 2)) + "," + str(round(float(auth_num), 2))
        user.save()

    context = {
    'form': form
    }

    return render(request, "users/quiz.html", context)

def feedback_view(request):
    form = FeedbackForm(request.POST or None, instance = request.user)
    if form.is_valid():
        form.save()
        message = Feedback.objects.create(message=form.cleaned_data, sender=request.user)
        message.save()
        messages.success(request, f'Thanks for the feedback!')
        return redirect('chat:chathome')

    context = {
    'form': form
    }

    return render(request, "users/feedback.html", context)
