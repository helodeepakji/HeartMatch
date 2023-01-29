from django.shortcuts import redirect, render
from datetime import datetime
from app.models import Contact,Cuser,Friend
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout

def index(request):
    return render(request,"index.html")


def about(request):
    return render(request,"about.html")


def userlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            context = {"status":"User not found"}
            return render(request,"login.html",context) 
    else:
        if request.user.is_authenticated:
            return redirect(profile)
        return render(request,"login.html")


def regisiter(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        occupation = request.POST.get('occupation')
        salary = request.POST.get('salary')
        education = request.POST.get('education')
        profile = request.FILES.get('profile')
        city = request.POST.get('city')
        age = request.POST.get('age')
        state = request.POST.get('state')
        reigion = request.POST.get('reigion')
        mothertoug = request.POST.get('mothertoug')
        if cpassword != password:
            context = {"status":"Password is not equal to confirm password"}
            return render(request,"regisiter.html",context)
        mydata = Cuser.objects.filter(username=username).values() | Cuser.objects.filter(email=email).values() | Cuser.objects.filter(phone=phone).values()
        if mydata :
            context = {"status":"user already found"}
            return render(request,"regisiter.html",context)
        else:
            cuser = Cuser(name=name,username=username,email=email,phone=phone,gender=gender,password=password,occupation=occupation,salary=salary,education=education,city=city,age=age,state=state,reigion=reigion,image=profile,mothertoug=mothertoug)
            cuser.save()
            user = User.objects.create_user(username,email,password)
            user.save()
            login(request, user)
            return redirect(index)
    else:
        return render(request,"regisiter.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        query = request.POST.get('query')
        contact = Contact(name=name,email=email,phone=number,query=query,date=datetime.today())
        contact.save()
        context = {"submit":contact}
        return render(request,"contact.html",context)
    else:
        return render(request,"contact.html")


def profile(request):
    if request.user.is_authenticated:
        lst = []
        data = Cuser.objects.filter(username=request.user).values()
        friend = Friend.objects.filter(touser=request.user).values()
        alldata = Cuser.objects.all().values()
        for person in friend :
            if person['request'] == False:
                for match in alldata :
                    if person['username'] == match['username']:
                        lst.append(match)

        context = {"data":data[0],"friend" : lst}
        return render(request,"profile.html",context)
    else:
        return redirect(userlogin)


def userlogout(request):
    logout(request)
    return redirect(index)


def editprofile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('name')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            education = request.POST.get('education')
            occupation = request.POST.get('occupation')
            reigion = request.POST.get('reigion')
            mothertoug = request.POST.get('mothertoug')
            city = request.POST.get('city')
            state = request.POST.get('state')
            cuser = Cuser.objects.get(username=request.user)
            cuser.name = name
            cuser.age = age
            cuser.email = email
            cuser.phone = phone
            cuser.education = education
            cuser.occupation = occupation
            cuser.reigion = reigion
            cuser.mothertoug = mothertoug
            cuser.city = city
            cuser.state = state
            cuser.save()
            return redirect(profile)



def findbest(request):
    if request.method == "POST":
        print(request.POST.get)
        cuser = Cuser.objects.filter(mothertoug=request.POST.get('mother_tong'),gender=request.POST.get('gender'),reigion=request.POST.get('reigion'),state=request.POST.get('state')).values()
        context = {"data":cuser}
        return render(request,"findbest.html",context)
    elif request.user.is_authenticated:
            cuser = Cuser.objects.all().exclude(username=request.user).values() 
            addfriend = Friend.objects.filter(username=request.user).values() 
            print(addfriend)
            context = {"data":cuser,"addfriend":addfriend}
            return render(request,"findbest.html",context)          
    else :
        cuser = Cuser.objects.all().values()
        context = {"data":cuser}
        return render(request,"findbest.html",context)  



#api for ajax

def addFriend(request):
    if request.user.is_authenticated:
        user = str(request.user)
        username = request.GET.get('username')
        room = username+user
        addfriend = Friend.objects.filter(username=user,touser=username).values()
        if len(addfriend) == 0 :
            friend = Friend(username = user,touser = username,room = room,request = False,date = datetime.today())
            friend.save()
        response = {
            'is_taken': "success"
        }
        return JsonResponse(response)


def acceptFriend(request):
    if request.user.is_authenticated:
        user = str(request.user)
        username = request.GET.get('username')
        addfriend = Friend.objects.filter(username=user,touser=username).values()
        if len(addfriend) == 0 :
            addfriend = Friend(username = friend['touser'],touser = friend['username'],room = friend['room'],request = True,date = datetime.today())
            friend = Friend.objects.filter(username=username,touser=user)[0]
            friend.request = True
            friend.save()
        else :
            friend = Friend.objects.filter(username=username,touser=user)[0]
            addfriend = Friend.objects.filter(username=user,touser=username)[0]
            addfriend.room = friend.room
            addfriend.request = True
            addfriend.save()
            friend.request = True
            friend.save()
        response = {
            'is_taken': True
        }
        return JsonResponse(response)

