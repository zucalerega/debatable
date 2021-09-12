from django.shortcuts import render, redirect
from chat.models import Room, Message, Rating
from django.http import HttpResponse, JsonResponse
from datetime import datetime
import time
import random
import string
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest
from users.models import Profile
from django.contrib.auth.models import User
import numpy as np
from itertools import chain
from posts.models import Post, Like
from users.models import Follow
def match(searching_users):
    for searching_user in searching_users.reverse():
        f_ideology = searching_users.reverse()[0].ideology.split(",")
        ideology = searching_user.ideology.split(",")
        if ((float(f_ideology[0])-float(ideology[0]))**2 + (float(f_ideology[1])-float(ideology[1]))**2)**0.5 >= 1:
            #print(2)
            if searching_user.topic == searching_users.reverse()[0].topic:
                #print(3)
                if searching_user.style == searching_users.reverse()[0].style:
                    if searching_users[0] != searching_users[1]:
                        return [searching_users.reverse()[0], searching_user]
    return []
    #return [searching_users[0], searching_users[1]]
def ajax_required(f):
   """
   AJAX request required decorator
   use it in your views:

   @ajax_required
   def my_view(request):
       ....

   """

   def wrap(request, *args, **kwargs):
       if not request.is_ajax():
           return redirect('/chat/')
       return f(request, *args, **kwargs)

   wrap.__doc__=f.__doc__
   wrap.__name__=f.__name__
   return wrap

def stop_search(request):
    user = Profile.objects.get(user=request.user)
    user.searching = False
    user.save()
# The way to use this decorator is:

# Create your views here.
#@login_required
def home(request):
    stop_search(request)
    temp = []
    for i in Room.objects.all():
        if i.aut != None:
            if request.user.username in i.aut:
                temp.append(i)
    queryset = list(chain(Room.objects.filter(auo=request.user), Room.objects.filter(aut=request.user), temp))
    message_list = {}
    for i in queryset:
        if len(Message.objects.filter(room=i.id)) > 0:
            message_list[i] = Message.objects.filter(room=i.id).order_by('-date')[0]
        else:
            message_list[i] = 'No messages yet'

    if request.user != 'AnonymousUser':
        basic_suggestions = []
        for i in Follow.objects.filter(follower = request.user):
            for j in Post.objects.filter(author = i.following):
                basic_suggestions.insert(0, [j, (len(Like.objects.filter(post=j, action=True))- len(Like.objects.filter(post=j, action=False)))])

    group_rooms = {}
    like_list = []
    dislike_list = []

    for like in Like.objects.filter(actor=request.user):
        if like.action == True:
            like_list.append(like.post)
        else:
            dislike_list.append(like.post)
    for room in Room.objects.filter(group_room=True):
        group_rooms[room] = room.aut.split(',')
    context = {
        "basic_suggestions": basic_suggestions,
        "object_list": queryset,
        "message_list": message_list,
        "searching_users":len(Profile.objects.filter(searching=True)),
        "group_rooms": group_rooms,
        "like_list": like_list,
        "dislike_list": dislike_list
        }
    return render(request, "chathome.html", context)

#@login_required
def room(request, room):
    if Room.objects.get(name=room).group_room == False:
        searching_user = Profile.objects.get(user=request.user)
        room_obj = Room.objects.get(name=room)
        if room_obj.auo.replace(' Profile', '') == searching_user.user.username or room_obj.aut.replace(' Profile', '') == searching_user.user.username:
           pass
        else:
           return redirect('/chat/')

        searching_user.searching = False
        searching_user.save()
        username = request.GET.get('username')
        room_details = Room.objects.get(name=room)
        if str(room_obj.auo) == str(request.user):
            opponent = Profile.objects.get(user=User.objects.get(username=room_obj.aut.replace(' Profile', '')))
            me = Profile.objects.get(user=User.objects.get(username=room_obj.auo.replace(' Profile', '')))
        else:
            opponent = Profile.objects.get(user=User.objects.get(username=room_obj.auo.replace(' Profile', '')))
            me = Profile.objects.get(user=User.objects.get(username=room_obj.aut.replace(' Profile', '')))
        temp = []
        for i in Room.objects.all():
            if i.aut != None:
                if request.user.username in i.aut:
                    temp.append(i)
        queryset = list(chain(Room.objects.filter(auo=request.user), Room.objects.filter(aut=request.user), temp))
        message_list = {}
        for i in queryset:
            if len(Message.objects.filter(room=i.id)) > 0:
                message_list[i] = Message.objects.filter(room=i.id).order_by('-date')[0]
            else:
                message_list[i] = 'No messages yet'

        totalratings = len(Rating.objects.filter(recipient=str(opponent.user)))
        return render(request, 'room.html', {
            "message_list": message_list,
            "username": username,
            "room": room,
            "room_details": room_details,
            "opponent": opponent,
            "totalratings": totalratings,
            "me": me,
            "messages": queryset
        })
    else:
        searching_user = Profile.objects.get(user=request.user)
        searching_user.searching = False
        searching_user.save()
        username = request.GET.get('username')
        room_details = Room.objects.get(name=room)
        if searching_user.user.username not in room_details.aut:
            room_details.aut +=  ',' + searching_user.user.username
            room_details.save()
        temp = []
        for i in Room.objects.all():
            if i.aut != None:
                if request.user.username in i.aut:
                    temp.append(i)
        queryset = list(chain(Room.objects.filter(auo=request.user), Room.objects.filter(aut=request.user), temp))
        message_list = {}
        for i in queryset:
            if len(Message.objects.filter(room=i.id)) > 0:
                message_list[i] = Message.objects.filter(room=i.id).order_by('-date')[0]
            else:
                message_list[i] = 'No messages yet'
        return render(request, 'group_room.html', {
            "message_list": message_list,
            "username": username,
            "room": room,
            "room_details": room_details,
            "messages": queryset
        })

def checkview(request):
    if request.POST.get('group_room', False) == "True":
        if len(Room.objects.filter(topic=request.POST['topic'])) == 1:
            room = Room.objects.get(topic=request.POST['topic'])
            return redirect('/chat/' + room.name + '/')

        room = Room.objects.create(name=''.join(random.choice(string.ascii_letters) for i in range(16)), topic=request.POST['topic'], auo=request.user, aut=request.user, group_room=True)
        return redirect('/chat/' + room.name + '/')

    searching_user = Profile.objects.get(user=request.user)
    searching_user.room = 'null'
    searching_user.topic = request.POST.get('topic', 'general')
    searching_user.style = request.POST.get('chat-style', 'general')

    #print(searching_user.searching)
    searching_user.searching = True
    searching_user.save()
    searching_users = []
    #print(Profile.objects.filter(searching = True))
    while len(searching_users) < 2:
        try:
            searching_users = match(Profile.objects.filter(searching = True))
        except IndexError:
            searching_users = []
    print(searching_users)
    for i in searching_users:
        i.room = str(searching_users[0].user.id) + str(searching_users[1].user.id) + str(searching_users[0].user.id*searching_users[1].user.id) + str(searching_users[0].user.id+searching_users[1].user.id)
        #print(i, i.room)
        i.save()
    room = request.POST.get('room_name', i.room)
    if Room.objects.filter(name=room).exists():
        return redirect('/chat/' + room + '/')
    new_room = Room.objects.create(name=room, auo=searching_users[0].user.username, aut = searching_users[1].user.username, topic=request.POST.get('topic', 'general'))
    new_room.save()
    return redirect('/chat/' + room + '/')

def send(request):
    message = request.POST['message']
    #username = request.POST['username']
    room_id = request.POST['room_id']
    now = datetime.now()
    new_message = Message.objects.create(value=message, user=request.user, room=room_id, sender=request.user.username)
    new_message.save()
    return HttpResponse('Message sent yeeyye')

@ajax_required
def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})


def rateview(request, room):
    if len(Rating.objects.filter(recipient = request.POST['opponent'], rating = int(request.POST['rating']))) == 0:
        new_rating = Rating.objects.create(
        rater = request.user.username,
        recipient = request.POST['opponent'],
        rating = int(request.POST['rating']),
        message = request.POST['feedback']
        )
        opponent = Profile.objects.get(user=User.objects.get(username=request.POST['opponent']))
        # if int(request.POST['rating']) > 5:
        #     opponent.rating = opponent.rating + np.sqrt(int(request.POST['rating'])*int(Profile.objects.get(user=User.objects.get(username=request.user)).rating))
        # elif int(request.POST['rating']) < 5:
        #     if (opponent.rating - np.sqrt(int(request.POST['rating'])*int(Profile.objects.get(user=User.objects.get(username=request.user)).rating))) >= 1:
        #         opponent.rating = opponent.rating - np.sqrt((10-int(request.POST['rating']))*int(Profile.objects.get(user=User.objects.get(username=request.user)).rating))
        #     else:
        #         opponent.rating = 1
        r_sum = 0
        for i in Rating.objects.filter(recipient=str(opponent.user)):
            r_sum += i.rating

        opponent.rating = r_sum/len(Rating.objects.filter(recipient=str(opponent.user)))
        opponent.save()
    return redirect("/chat/")

def report(request, message, room):
    banned_words = ['fuck',
    'porn'
    ]
    reporter = Profile.objects.get(user=User.objects.get(username=request.user))
    offender = Profile.objects.get(user=message.user)
    for word in banned_words:
        if word in message.value:
            message.reported = True
            message.save()
    print(message.reported)
    return redirect("/chat/" + room + "/")

def leaveview(request, room):
    user = "," + request.user.username
    left_room = Room.objects.get(name=room)
    left_room.aut = left_room.aut.replace(user, '')
    left_room.auo = left_room.auo.replace(user, '')
    left_room.save()
    print(left_room.aut)

    return redirect("chat:chathome")
