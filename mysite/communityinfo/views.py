from django.contrib.auth import authenticate
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from .forms import RegistrationForm, LoginForm, CommunityCreationForm, EditRulesForm, TextBasedPostForm
from .models import Community, UserCommunity, RegisteredUser, UserFollower, Posts, Comments
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST.getlist('email')[0],
                                        password=request.POST.getlist('password')[0])
        user.save()
        registered_user = RegisteredUser.objects.create(email=request.POST.getlist('email')[0],
                                                        password=request.POST.getlist('password')[0])
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

    return render(request, 'home.html', {'communities': communities, 'people': people, 'username': username,
                                         'posts': posts, 'user_communities':user_communities})


def community_creation(request):
    username = request.session['username']
    if request.method == 'POST':
        community = Community.objects.create(name=request.POST.getlist('name')[0],
                                             description=request.POST.getlist('description')[0],
                                             privacy=request.POST.getlist('privacy')[0],
                                             rules=request.POST.getlist('rules')[0],
                                             creator=username)
        community.save()
        form = CommunityCreationForm()
        return render(request, 'join-community.html', {'form': form})
    else:
        form = CommunityCreationForm()
        return render(request, 'community-creation.html', {'form': form})


def edit_rules(request, community_name):
    community = Community.objects.get(name=community_name)
    if request.method == 'POST':
        form = EditRulesForm(request.POST, instance=community)
        if form.is_valid():
            form.save()
            return render(request, 'home.html')  # Redirect to home page or wherever you want after editing rules
    else:
        form = EditRulesForm(instance=community)
    return render(request, 'edit-rules.html', {'form': form, 'community_name': community_name, 'rules': community.rules})

'''
def join_community(request, community_name):
    if request.method == 'POST':
        username = request.session['username']
        # Create a Community_Creation object
        community_enrollment = UserCommunity.objects.create(username=username, community_name=community_name)
        community_enrollment.save()
        posts = Posts.objects.filter(community_name=community_name)
        community = Community.objects.filter(name=community_name)
        rules = community[0].rules
        creator = community[0].creator

        # Retrieve comments for each post
        for post in posts:
            post.comments = Comments.objects.filter(post_id=post.id)
        comments = Comments.objects.all()

        return render(request, 'join-community.html', {'community_name': community_name,
                                                       'posts': posts, 'comments': comments,
                                                       'rules': rules, 'username': username, 'creator': creator})
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
        community = Community.objects.filter(name=community_name)
        rules = community[0].rules

        return render(request, 'visit-community.html', {'community_name': community_name, 'posts': posts,
                                                        'comments': comments, 'rules': rules})
    else:
        # Handle the case when the request method is not POST
        # This can include displaying an error message or redirecting the user
        pass
'''


def community(request, community_name):
    username = request.session.get('username')
    user_joined = UserCommunity.objects.filter(username=username, community_name=community_name).exists()
    community = Community.objects.get(name=community_name)

    if user_joined:
        # User has joined the community, allow them to create posts
        if request.method == 'POST':
            form = TextBasedPostForm(request.POST)
            if form.is_valid():
                header = form.cleaned_data['header']
                description = form.cleaned_data['description']
                post_to_share = Posts.objects.create(community_name=community_name, submitter_name=username,
                                                     header=header, description=description,
                                                     number_of_upvotes=0, number_of_downvotes=0,
                                                     number_of_smiles=0, number_of_hearts=0, number_of_sadfaces=0)
                post_to_share.save()
                return redirect('community', community_name=community_name)
        else:
            form = TextBasedPostForm()

        posts = Posts.objects.filter(community_name=community_name)
        comments = Comments.objects.all()

        return render(request, 'community.html', {
            'community_name': community_name,
            'community': community,
            'user_joined': user_joined,
            'username': username,
            'posts': posts,
            'comments': comments,
            'form': form,
        })
    else:
        # If the user hasn't joined the community, redirect them to the home page or show an error message
        return redirect('home_page')


def join_community(request, community_name):
    if request.method == 'POST':
        username = request.session.get('username')
        user_joined = UserCommunity.objects.filter(username=username, community_name=community_name).exists()
        if not user_joined:
            # User is not already a member of the community, add them and redirect to community page
            UserCommunity.objects.create(username=username, community_name=community_name)
        return redirect('community', community_name=community_name)
    else:
        # Handle the case when the request method is not POST
        # This can include displaying an error message or redirecting the user
        pass


def visit_community(request, community_name):
    username = request.session.get('username')
    user_joined = UserCommunity.objects.filter(username=username, community_name=community_name).exists()
    community = get_object_or_404(Community, name=community_name)

    posts = Posts.objects.filter(community_name=community_name)
    comments = Comments.objects.all()

    return render(request, 'visit-community.html', {
        'community_name': community_name,
        'community': community,
        'user_joined': user_joined,
        'username': username,
        'posts': posts,
        'comments': comments,
    })


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
        return render(request,'search-communities.html', {"users": registered_users, "communities": communities})
    else:
        return redirect('home')


def share_post(request, community_name):
    username = request.session.get('username')

    if request.method == 'POST':
        form = TextBasedPostForm(request.POST)
        if form.is_valid():
            header = form.cleaned_data['header']
            description = form.cleaned_data['description']
            post_to_share = Posts.objects.create(community_name=community_name, submitter_name=username,
                                                 header=header, description=description,
                                                 number_of_upvotes=0, number_of_downvotes=0,
                                                 number_of_smiles=0, number_of_hearts=0, number_of_sadfaces=0)
            post_to_share.save()
        return render(request,'community.html', {'community_name': community_name})
    else:
        form = TextBasedPostForm()

    return render(request, 'share-post.html', {'form': form})

