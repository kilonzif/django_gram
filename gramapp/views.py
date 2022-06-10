from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout

from gramapp.models import Profile

# Create your views here.


def home(request):
    return render (request, 'index.html')

def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"] 
        
        user = authenticate (request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You are successfuly logged in")
            return redirect ("/")
    return render (request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]

        if password1 != password2:
            messages.error(request,"Passwords do not match")
            return redirect('/register')

        new_user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1

        )
        new_user.save()

        new_profile = Profile.objects.create(
            user=new_user,
            bio="",
            profile_picture="",
        )
        new_profile.save()
        return render(request,'login.html')

    return render (request, 'register.html')


def signout(request):
    logout(request)
    messages.success(request,"You have logged out")
           
    return redirect("/")

@login_required
def profile(request):
    user = request.user
    my_profile = Profile.objects.get(user=user)
    print(my_profile)
    return render(request,"profile.html",{'my_profile':my_profile,'user':user})


@login_required
def update_profile(request):
    user = request.user
    if request.method=="POST":
        bio = request.POST["bio"]
        profile_picture =request.FILES["profile_picture"]
        my_profile = Profile.objects.get(user=user)
        my_profile.save()

    return redirect("/profile")


 