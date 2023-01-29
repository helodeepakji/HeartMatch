from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
# Create your views here.
from django.shortcuts import render
from app.models import Friend, Cuser
from chat.models import Chat

def index(request):
    if request.user.is_authenticated:
        friends = Friend.objects.filter(username = request.user).values()
        cuser = Cuser.objects.all().values()
        return render(request, "chat/index.html",{"friends":friends,"cusers" : cuser})

def room(request, room_name):
    if request.user.is_authenticated:
        n = len(str(request.user))
        touser = room_name[:-n]
        user = room_name[n:]
        
        if str(request.user) == str(room_name[len(touser):]) :
            user = str(room_name[len(touser):])
            touser = str(room_name[:-len(user)])

        if str(request.user) == str(room_name[:-len(touser)]) :
            user = str(room_name[:-len(touser)])
            touser = str(room_name[len(user):])
        
        if str(request.user) == user:
            friends = Friend.objects.filter(username = request.user).values()
            cuser = Cuser.objects.all().values()
            friendreq = Friend.objects.filter(touser=touser).values()
            if len(friendreq) == 0 :
                return redirect(index)

            friendreq = friendreq[0]
                
            if friendreq['request'] :
                touser = Cuser.objects.filter(username = touser).values()
                touser = touser[0]
                chat = Chat.objects.filter(room = room_name).order_by('datetime').values()
                return render(request, "chat/room.html", {"room_name": room_name,"friends":friends,"cusers" : cuser, "touser":touser,"chat":chat})
        
        return redirect(index)

    else:
        return redirect(index)