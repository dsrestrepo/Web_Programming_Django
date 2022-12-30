from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Followers, Likes
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        total_posts = posts.order_by("-timestamp").all()
        paginator = Paginator(total_posts, 10) # Show 10 post per page.
    
        likeds={}
        total_likes={}
        for post in total_posts:
            try:
                likes=Likes.objects.get(post=post)
            except Likes.DoesNotExist:
                likes = Likes.objects.create(post=post)
            try:
                liked = Likes.objects.filter(post=post,users=request.user)
            except Likes.DoesNotExist:
                liked = False
            if not liked:
                liked=False
            likeds[post.id] = liked
            total_likes[post.id]= likes.users.all().count()
        print(total_likes)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'network/index.html', {
            'page_obj': page_obj,
            'total_likes':total_likes,
            'likeds':likeds
        })
    else:
        posts = Post.objects.all()
        total_posts = posts.order_by("-timestamp").all()
        paginator = Paginator(total_posts, 10) # Show 10 post per page.
    
        likeds={}
        total_likes={}
        for post in total_posts:
            try:
                likes=Likes.objects.get(post=post)
            except Likes.DoesNotExist:
                likes = Likes.objects.create(post=post)
            total_likes[post.id]= likes.users.all().count()
        print(total_likes)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'network/index.html', {
            'page_obj': page_obj,
            'total_likes':total_likes,
        })

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



@csrf_exempt
@login_required
def newPost(request):
    # Composing new post, methond == POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    content = data.get("content", "")
    newpost=Post(user=request.user, content=content)
    newpost.save()
    return JsonResponse({"message": "Post successfully."}, status=201)

@login_required
def users(request,username):
    if request.method != "GET":
        return JsonResponse({
            "error": "GET request required."
        }, status=400)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    print(user)
    return JsonResponse(user.serialize(), safe=False)


@login_required
def profiles(request):
    users=User.objects.all()
    return render(request, 'network/profiles.html',{
        'users':users,
    })

@login_required
def profile(request,username):
    user=User.objects.get(username=username)
    
    #count the number of followers
    try:
        followers = Followers.objects.get(user=user)
    except  Followers.DoesNotExist:
        followers = Followers.objects.create(user=user)
    totalfollowers = followers.followers.all().count()
    #see if the user requesting alredy follows the user of the profile
    try:
        is_following=Followers.objects.get(user=user,followers=request.user)
    except Followers.DoesNotExist:
        is_following=None
    #count the number of following
    try:
        following = Followers.objects.filter(followers=user)
    except  Followers.DoesNotExist:
        following = None
    totalfollowing = following.count()
    
    #take the posts of the user
    posts = user.posts.all()
    total_posts = posts.order_by("-timestamp").all()
    paginator = Paginator(total_posts, 10) # Show 10 post per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #take the actual user to see if user has hit like to some post
    actual_User=request.user
    total_likes={}
    likeds={}
    for post in total_posts:
        try:
            likes = Likes.objects.get(post=post)
        except Likes.DoesNotExist:
            likes = Likes.objects.create(post=post)
        
        try:
            liked = Likes.objects.filter(post=post,users=actual_User)
        except Likes.DoesNotExist:
            liked = False
        if not liked:
            liked=False
        likeds[post.id] = liked
        total_likes[post.id] = likes.users.all().count()
    print(total_likes)
    print(likeds)
    return render(request, 'network/profile.html',{
        'user_profile':user,
        'followers':followers,
        'totalfollowers':totalfollowers,
        'totalfollowing':totalfollowing,
        'page_obj': page_obj,
        'total_likes':total_likes,
        'likeds':likeds,
        'is_following':is_following
    })

@login_required
def following(request):
    try:
        following = Followers.objects.filter(followers=request.user)
    except  Followers.DoesNotExist:
        following = None
    if not following:
        return render (request,'network/notFollowing.html')
    if following == None:
        return render (request,'network/notFollowing.html')
    users=[]
    for following_user in following:
        users.append(following_user.user)
        print(users)
    posts=Post.objects.filter(user__in=users)
    total_posts = posts.order_by("-timestamp").all()
    paginator = Paginator(total_posts, 10) # Show 10 post per page.
    
    likeds={}
    total_likes={}
    for post in total_posts:
        try:
            likes=Likes.objects.get(post=post)
        except Likes.DoesNotExist:
            likes = Likes.objects.create(post=post)
        try:
            liked = Likes.objects.filter(post=post,users=request.user)
        except Likes.DoesNotExist:
            liked = False
        if not liked:
            liked=False
        likeds[post.id] = liked
        total_likes[post.id]= likes.users.all().count()
    print(total_likes)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', {
        'page_obj': page_obj,
        'total_likes':total_likes,
        'likeds':likeds
    })

@csrf_exempt
@login_required
def edit_post(request, post_id):
    # Query for post
    try:
        post=Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    try:
        post=Post.objects.get(id=post_id,user=request.user)#just owner can edit
    except Post.DoesNotExist:
        return JsonResponse({"error": "you can't edit other user's post"}, status=404)
    # Return post if get
    if request.method == "GET":
        return JsonResponse(post.serialize())
    # Update post
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return JsonResponse({"message": "Post Edited"}, status=201)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt
@login_required
def like(request, post_id):
    # Query for post
    try:
        post=Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    #query likes of the post
    try:
        likes=Likes.objects.get(post=post)
    except Likes.DoesNotExist:
        likes=Likes.objects.create(post=post)
    # Update post
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like") is not None:
            if data['like']:
                likes.users.add(request.user)
            else:
                likes.users.remove(request.user)

        return JsonResponse({"message": "like state changed"}, status=201)                
        #return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def follow(request, username):
    #take the row of followers for the user or create the row
    try:
        user=User.objects.get(username=username)
    except  User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    #take the row of followers for the user or create the row
    try:
        followers = Followers.objects.get(user=user)
    except  Followers.DoesNotExist:
        followers = Followers.objects.create(user=user)

    # Add or Remove user to followers
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("follow") is not None:
            if data["follow"]:
                followers.followers.add(request.user)
            else:
                followers.followers.remove(request.user)
                
        return JsonResponse({"message": "Follow state changed"}, status=201)    
        #return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)