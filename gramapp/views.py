from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import *
from gramapp.models import Profile, Post, Comment, Likes

# Create your views here.


def home(request):
    posts = Post.objects.all()

    ctx = {
        "posts": posts
    }
    return render(request, 'index.html', ctx)


def add_post(request):
    form = PostForm()

    current_user = request.user
    user = Profile.objects.get(user=current_user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            post = form.save(commit=False)

            post.user_id = user

            post.save()

            return redirect('/')
        else:
            form = PostForm()

    ctx = {
        'form': form
    }

    return render(request, 'add_post.html', ctx)


def view_post(request, post_id):
    post = Post.objects.get(id=post_id)
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    post_comments = Comment.objects.filter(post_id=post_id)
    likes_count = Likes.objects.filter(post_id=post_id).count()
    liked = False

    try:

        like = Likes.objects.filter(post_id=post_id, user_id=user.id)

        if like:
            liked = True
        else:
            liked = False

    except Likes.DoesNotExist:
        print('')

    # get post comment

    ctx = {
        'post': post,
        'post_comments': post_comments,
        'likes_count': likes_count,
        'liked': liked

    }
    return render(request, 'view_post.html', ctx)


def add_post_comment(request, post_id):

    current_user = request.user
    user = User.objects.get(username=current_user.username)
    post = Post.objects.get(id=post_id)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():

            # form.save()
            comment = form.save(commit=False)

            comment.user_id = user
            comment.post_id = post

            comment.save()

            return redirect('/')
        else:
            form = CommentForm()

    ctx = {
        'form': form,
        'post': post
    }

    return render(request, 'add_post_comment.html', ctx)


def like_post(request, post_id):

    current_user = request.user
    user = User.objects.get(username=current_user.username)
    post = Post.objects.get(id=post_id)

    try:

        like = Likes.objects.filter(post_id=post_id, user_id=user.id)

        if like:
            like.delete()
        else:
            Likes.objects.create(
                user_id=user,
                post_id=post
            )

    except Likes.DoesNotExist:
        print('')

    return redirect('view_post', post_id=post.id)


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are successfuly logged in")
            return redirect("/")
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match")
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
        return render(request, 'login.html')

    return render(request, 'register.html')


def signout(request):
    logout(request)
    messages.success(request, "You have logged out")

    return redirect("/")


@login_required(login_url='/login/')
def profile(request):

    # testuser

    # hmugera
    user = request.user

    my_profile = Profile.objects.get(user=user)

    print(my_profile)
    return render(request, "profile.html", {'my_profile': my_profile, 'user': user})


@login_required
def user_profile(request, id):

    user = User.objects.get(id=id)
    
    
    if request.user ==user:
        return redirect("/profile")
        

    my_profile = Profile.objects.get(user=user)

    return render(request, "user_profile.html", {'my_profile': my_profile, 'user': user})


@login_required
def update_profile(request):
    user = request.user
    if request.method == "POST":
        bio = request.POST["bio"]
        profile_picture = request.FILES["profile_picture"]
        my_profile = Profile.objects.get(user=user)
        my_profile.save()

    return redirect("/profile")
