from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "chat/index.html")

def room(request, room_name):
    if request.user.is_authenticated:
        return render(request, "videocall/index.html")