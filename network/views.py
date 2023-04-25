import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Comments, Follower, Likes


def index(request):
    
    user = request.user
    
    #post is used to make a new posting to the page
    if request.method == 'POST':
        post = request.POST['post']
        new_post = Post(content=post, user=user)
        new_post.save()
    
    #get posts from table and paginate them
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    
    #default page number is 1
    page_num = 1
    
    #if request method is get then get the page the user has selected
    if request.method == 'GET':
        page_num = request.GET.get('page')
    
    #get the correct page view from paginator and render
    page = paginator.get_page(page_num)
    return render(request, "network/index.html", {
        'page':page,
        'user':user
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


def Profile_page(request, page_id):
    
    user = request.user
    
    # default your_page is false but checks to see if you're on your page and if so change to true.
    # no follow button on your own page... you can't follow yourself.
    your_page = False
    if page_id == request.user.id:
        your_page = True
    
    # get owner of profile page you are currently on
    page_user = User.objects.get(id=page_id)
    
    followers = user.followers.all()
    print(followers)

    # check if user is following the profile page owner to change follow button to unfollow if true
    users_following_profile = page_user.followers.all()
    follower_count = len(users_following_profile)

    following_count = len(page_user.following.all())
    
    following_user = user.following.filter(following=page_id)
    following = False
    if not your_page:
        print('not your page')
        if following_user:
            print("following")
            following = True
    
    # get posts for profile based on page_id
    posts = Post.objects.filter(user=page_id).order_by('-timestamp')
    
    paginator = Paginator(posts, 10)
    
    #default page number is 1
    page_num = 1
    
    #if request method is get then get the page the user has selected
    if request.method == 'GET':
        page_num = request.GET.get('page')
    
    #get the correct page view from paginator and render
    page = paginator.get_page(page_num)
    
    return render(request, 'network/profile.html',{
        'your_page': your_page,
        'posts': posts,
        'page_user':page_user,
        'following':following,
        'follower_count':follower_count,
        'following_count':following_count,
        'page':page,
        'user':user
    })


@login_required(login_url='/login')
def Follow(request):
    id = request.POST.get('id')
    user = request.user
    
    if request.method == 'POST':
        #take id and look up associated user
        user_to_follow = User.objects.filter(id=id).first()
                
        #check to see if user is following already
        is_following = Follower.objects.filter(user=user, following=user_to_follow).first()
        if is_following:
            is_following.delete()

        #if user is not following, add user and user-to-follow to Follower table
        else:
            new_follower = Follower(user=user, following=user_to_follow)

            #save following table
            new_follower.save()

        #redirect back to profile you came from    
        return HttpResponseRedirect(reverse('Profile_page', kwargs={'page_id':id}))

    else:    
        followed_by_user = user.following.all()
        if not followed_by_user:
            follows = False
        else:
            follows = True
        posts = []
        for i in followed_by_user:
            followed_user = i.following
            user_posts = followed_user.posts.all()
            for post in user_posts:
                posts.append(post)
           
        posts.sort(key=lambda x: x.timestamp, reverse=True)
        
        paginator = Paginator(posts, 10)

        #default page number is 1
        page_num = 1

        page_num = request.GET.get('page')

        #get the correct page view from paginator and render
        page = paginator.get_page(page_num)
        if not posts:
            posts = None
        
        return render(request, 'network/follow.html', {
            'posts':posts,
            'follows':follows,
            'page':page
        })


def edit(request):
    user = request.user
    data = json.loads(request.body)
    post_id = data.get('post_id', '')
    post = Post.objects.get(id=post_id)
    if user == post.user:
        content = data.get('content', '')
        print(content)
        post.content = content
        post.save()
        return JsonResponse({'success': 'yay!'}, status=200)
    else:
        return JsonResponse({'error': 'You do not have authorization to edit this post.'}, status=403)


def like(request):
    user = request.user
    data = json.loads(request.body)
    print(data)
    post_id = data.get('post_id', '')
    post = Post.objects.get(id=post_id)
    user_likes = user.likes.all()
    post_liked = False
    for i in user_likes:
        if post == i.liked_post:
            
            # Post has already been liked by the user
            post_liked = True
            break
    if post_liked:
        # Post has already been liked by the user
        like = user.likes.filter(liked_post=post)
        like.delete()
        post.likes_count = post.likes_count - 1
        post.save()
        return JsonResponse({'success': 'unliked', 'likes_count': post.likes_count}, status=200)
    else:
        # Post has not been liked by the user yet
        like = Likes(user=user, liked_post=post)
        like.save()
        post.likes_count = post.likes_count + 1
        post.save()
        print('went through but is not liked')
        return JsonResponse({'success': 'liked', 'likes_count': post.likes_count}, status=200)

    
