from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import Post, User



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def add_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        post = Post( content=content, owner=user)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/add_post.html")

# def likedis_post(request):
#     if request.method == "POST":
#         post_id = request.POST["post_id"]
#         post = Post.objects.get(id=post_id)
#         user = request.user
#         if user in post.liked_by.all():
#             post.liked_by.remove(user)
#         else:
#             post.liked_by.add(user)
#         return HttpResponseRedirect(reverse("index"))
#     else:
#         return render(request, "network/add_post.html")

# def likedis_post_fol(request):
#     if request.method == "POST":
#         post_id = request.POST["post_id"]
#         post = Post.objects.get(id=post_id)
#         user = request.user
#         if user in post.liked_by.all():
#             post.liked_by.remove(user)
#         else:
#             post.liked_by.add(user)
#         usert = request.user
#         following = usert.following.all()
#         posts = []
#         likes = []
#         for user in following:
#             for post in Post.objects.filter(owner=user):
#                 posts.append(post)
#                 likes.append(post.liked_by)
    
#         return render(request, "network/following.html", {
#             "posts": zip(reversed(posts), reversed(likes)),
#         })

# def likedis_post_prof(request, username):
#     if request.method == "POST":
#         post_id = request.POST["post_id"]
#         post = Post.objects.get(id=post_id)
#         user = request.user
#         if user in post.liked_by.all():
#             post.liked_by.remove(user)
#         else:
#             post.liked_by.add(user)
#         user_to_follow = User.objects.get(username=username)
#         posts = Post.objects.filter(owner=user_to_follow)
#         likes = []
#         for post in posts:
#             likes.append(post.liked_by)
#         return render(request, "network/user_profile.html", {
#             "user": user,
#             "username": username,
#             "posts": zip(reversed(posts), reversed(likes)),
#             "followers": user_to_follow.followers.all(),
#         })

def user_profile(request, username):
    user_to_follow = User.objects.get(username=username)
    posts = Post.objects.filter(owner=user_to_follow)
    likes = []
    for post in posts:
        likes.append(post.liked_by)
    return render(request, "network/user_profile.html", {
        "username": username,
        "posts": zip(reversed(posts), reversed(likes)),
        "followers": user_to_follow.followers.all(),
        "following": user_to_follow.following.all(),
    })
   

def follow(request, username):
    if request.method == "POST":
        user = request.user
        user_to_follow = User.objects.get(username=username)
        posts = Post.objects.filter(owner=user_to_follow)
        likes = []
        for post in posts:
            likes.append(post.liked_by)

        if user in user_to_follow.followers.all():
            user_to_follow.followers.remove(user)
            user.following.remove(user_to_follow)
        else:
            user_to_follow.followers.add(user)
            user.following.add(user_to_follow)
        return render(request, "network/user_profile.html", {
         "username": username,
         "posts": zip(reversed(posts), reversed(likes)),
         "followers": user_to_follow.followers.all(),
         "following": user_to_follow.following.all(),
     })

def following(request):
        
    usert = request.user
    if usert.is_authenticated:
        following = usert.following.all()
        posts = []
        likes = []
        for user in following:
            for post in Post.objects.filter(owner=user):
                posts.append(post)
                likes.append(post.liked_by)
        
        return render(request, "network/following.html", {
            "posts": zip(reversed(posts), reversed(likes)),
        })
    else:
        return HttpResponseRedirect(reverse("login"))

# def edit_post(request):
#     if request.method == "POST":
#         post_id = request.POST["post_id"]
#         post = Post.objects.get(id=post_id)
#         content = request.POST["content"]
#         post.content = content
#         post.save()
#         return HttpResponseRedirect(reverse("index"))

# def edit_post_prof(request):
#     if request.method == "POST":
#         post_id = request.POST["post_id"]
#         post = Post.objects.get(id=post_id)
#         content = request.POST["content"]
#         post.content = content
#         post.save()
#         user = request.user
#         user_to_follow = User.objects.get(username=user.username)
#         posts = Post.objects.filter(owner=user_to_follow)
#         posts = Post.objects.filter(owner=user_to_follow)
#         likes = []
#         for post in posts:
#             likes.append(post.liked_by)

#         return render(request, "network/user_profile.html", {
#          "username": user.username,
#          "posts": zip(reversed(posts), reversed(likes)),
#          "followers": user_to_follow.followers.all(),
#          "following": user_to_follow.following.all(),
#      })

#Paginator for posts 10 posts per page
def index(request):
    posts = Post.objects.all().order_by("created_at").reverse()
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    likes = []
    for post in posts:
        likes.append(post.liked_by)
    return render(request, "network/index.html", {
        "posts": zip(posts, likes),
        'popo' : posts
    })

# function to like or unlike a post then return a json response with the updated amount of likes for the post
def like_post(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            post_id = body["post_id"]
        except:
            post_id = request.POST["post_id"]
        post = Post.objects.get(id=post_id)
        user = request.user
        if user in post.liked_by.all():
            post.liked_by.remove(user)
            like = "Нравится"
        else:
            post.liked_by.add(user)
            like = "Не нравится"
        return JsonResponse({
            "likes": post.liked_by.count(),
            "like": like,
        })

#function to receive a json request with the post id and the new content of the post and update the post then return a json response with the updated post content
def edit_post_async(request): 
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            post_id = body["post_id"]
            content = body["content"]
        except:
            post_id = request.POST["post_id"]
            content = request.POST["content"]
        post = Post.objects.get(id=post_id)
        post.content = content
        post.save()
        return JsonResponse({
            "content": post.content,
        })
