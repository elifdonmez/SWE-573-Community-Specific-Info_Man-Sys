from django.contrib.auth import authenticate
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.db.models import Q

from .forms import RegistrationForm, LoginForm, CommunityCreationForm
from .models import Community, UserCommunity, RegisteredUser, UserFollower, Posts, Comments
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST.getlist('email')[0], password=request.POST.getlist('password')[0])
        user.save()
        registered_user = RegisteredUser.objects.create(email=request.POST.getlist('email')[0], password=request.POST.getlist('password')[0])
        registered_user.save()
        return redirect('login')  # Redirect to a success page
    else:
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.getlist('email')[0], password=request.POST.getlist('password')[0])
        if user is not None and check_password(request.POST.getlist('password')[0], user.password ):
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            # Redirect to a success page
            return redirect("home_page")
        else:
            # Invalid login
            return render(request, 'login.html', {'error_message': 'Invalid email or password.'})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def home_page(request):
    username = request.session['username']
    communities = Community.objects.all()
    people = RegisteredUser.objects.all()
    user_communities = UserCommunity.objects.filter(username=username).values_list('community_name', flat=True)

    # Retrieve people the user followed
    followed_users = UserFollower.objects.filter(username=username).values_list('follower_username', flat=True)

    # Retrieve posts from communities the user joined and people the user followed
    posts = Posts.objects.filter(
        models.Q(community_name__in=user_communities) | models.Q(submitter_name__in=followed_users))

    return render(request, 'home.html', {'communities': communities, 'people': people, 'username': username, 'posts': posts})


def community_creation(request):
    if request.method == 'POST':
        community = Community.objects.create(name=request.POST.getlist('name')[0],
                                             description=request.POST.getlist('description')[0],
                                             privacy=request.POST.getlist('privacy')[0])
        community.save()
    else:
        form = CommunityCreationForm()
        return render(request, 'communityCreation.html', {'form': form})


def join_community(request, community_name):
    if request.method == 'POST':
        username = request.session['username']
        # Create a Community_Creation object
        community_creation = UserCommunity.objects.create(username=username, community_name=community_name)
        community_creation.save()
        posts = Posts.objects.filter(community_name=community_name)

        # Retrieve comments for each post
        for post in posts:
            post.comments = Comments.objects.filter(post_id=post.id)
        comments = Comments.objects.all()

        return render(request, 'join_community.html', {'community_name': community_name, 'posts': posts, 'comments': comments})
    else:
        # Handle the case when the request method is not POST
        # This can include displaying an error message or redirecting the user
        pass


def visit_community(request, community_name):
    if request.method == 'POST':
        username = request.session['username']
        posts = Posts.objects.filter(community_name=community_name)
        # Retrieve comments for each post
        comments = Comments.objects.all()
            # print("Comment" + str(comments[0].comment_content))

        return render(request, 'visit_community.html', {'community_name': community_name, 'posts': posts, 'comments': comments})
    else:
        # Handle the case when the request method is not POST
        # This can include displaying an error message or redirecting the user
        pass

def follow_user(request, username):
    if request.method == 'POST':
        follower_username = request.session['username']
        follower_creation = UserFollower.objects.create(username=username, follower_username=follower_username)
        follower_creation.save()
        return render(request, 'follow-user.html', {'username': username})
    else:
        # Handle the case when the request method is not POST
        # This can include displaying an error message or redirecting the user
        pass


def search_communities(request):
    q = request.GET.get('q')
    if q:
        communities = Community.objects.filter(name__icontains=q)
        registered_users = RegisteredUser.objects.filter(email__icontains = q)
        return render(request,'search_communities.html', {"users": registered_users, "communities": communities})
    else:
        return redirect('home')
