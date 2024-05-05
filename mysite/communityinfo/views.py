from django.contrib.auth import authenticate
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from .forms import RegistrationForm, LoginForm, CommunityCreationForm, EditRulesForm, TextBasedPostForm, ProfileForm, \
    PostTemplateForm
from .models import Community, UserCommunity, RegisteredUser, UserFollower, Posts, Comments, UserProfile, PostTemplate
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


def view_profile(request):
    # Get the current user
    username = request.session['username']

    try:
        # Try to retrieve the user's profile
        user_profile = UserProfile.objects.get(email=username)
    except UserProfile.DoesNotExist:
        # If the profile does not exist, redirect to the edit profile page
        return redirect('edit_profile')
    user_photo = "/media/" + str(user_profile.photo).split("'")[1]

    return render(request, 'profile.html', {'user_profile': user_profile, 'user_photo': user_photo})


def edit_profile(request):
    # Get the current user
    username = request.session['username']

    try:
        # Retrieve the existing user profile instance
        user_profile = UserProfile.objects.get(email=username)
    except UserProfile.DoesNotExist:
        # If the profile does not exist, create a new one
        user_profile = UserProfile(email=username)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid() and request.FILES is not None:
            if len(request.FILES) > 0:
                # Update the user profile fields with the new data
                form.save()
            return redirect('view_profile')
    else:
        # Populate the form with the existing user profile data
        form = ProfileForm(instance=user_profile)

    return render(request, 'edit-profile.html', {'form': form})


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        # If user is registered, authanticate to the application
        if len(request.POST.getlist('email')) > 0 and len(request.POST.getlist('password')) > 0:
            user = authenticate(username=request.POST.getlist('email')[0], password=request.POST.getlist('password')[0])
            if user is not None and check_password(request.POST.getlist('password')[0], user.password ):
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                # Redirect to a success page
                return redirect("home_page")
            else:
                # Invalid login
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid email or password.'})
        else:
            # Invalid login
            return render(request, 'login.html', {'form': form, 'error_message': 'Invalid email or password.'})
    else:
        return render(request, 'login.html', {'form': form})


def home_page(request):
    # Get the current user
    username = request.session['username']
    # Get all existing communities
    communities = Community.objects.all()
    # Get all registered users
    people = RegisteredUser.objects.all()
    # Filter joined communities
    user_communities = UserCommunity.objects.filter(username=username).values_list('community_name', flat=True)
    # Retrieve people the user followed
    followed_users = UserFollower.objects.filter(follower_username=username).values_list('username', flat=True)
    # Retrieve posts from communities the user joined and people the user followed
    posts = Posts.objects.filter(
        models.Q(community_name__in=user_communities) | models.Q(submitter_name__in=followed_users))

    return render(request, 'home.html', {'communities': communities, 'people': people, 'username': username,
                                         'posts': posts, 'user_communities':user_communities,
                                         'followed_users': followed_users})


def community_creation(request):
    # Get the current user
    username = request.session['username']
    # Get all existing communities
    communities = Community.objects.all()
    # Filter joined communities
    people = RegisteredUser.objects.all()
    # Filter joined communities
    user_communities = UserCommunity.objects.filter(username=username).values_list('community_name', flat=True)
    # Retrieve people the user followed
    followed_users = UserFollower.objects.filter(username=username).values_list('follower_username', flat=True)
    # Retrieve posts from communities the user joined and people the user followed
    posts = Posts.objects.filter(
        models.Q(community_name__in=user_communities) | models.Q(submitter_name__in=followed_users))
    if request.method == 'POST':
        if len(request.POST.getlist('privacy')) > 0:
            is_private=request.POST.getlist('privacy')[0] == 'on'
        else:
            is_private= False
        # create community object
        community = Community.objects.create(name=request.POST.getlist('name')[0],
                                             description=request.POST.getlist('description')[0],
                                             privacy=is_private,
                                             rules=request.POST.getlist('rules')[0],
                                             creator=username)
        community.save()
        form = CommunityCreationForm()
        UserCommunity.objects.create(username=username, community_name=community.name)
        return render(request, 'home.html', {'form': form, 'communities': communities, 'people': people, 'username': username,
                                         'posts': posts, 'user_communities':user_communities})
    else:
        form = CommunityCreationForm()
        return render(request, 'community-creation.html', {'form': form})


def edit_rules(request, community_name):
    # Get current community object
    community = Community.objects.get(name=community_name)
    # Get posts of the current community
    posts = Posts.objects.filter(community_name=community_name)
    # Get all post comments
    comments = Comments.objects.all()
    # Get username
    username = request.session.get('username')
    # Get communities user joined
    user_joined = UserCommunity.objects.filter(username=username, community_name=community_name).exists()
    if request.method == 'POST':
        form = EditRulesForm(request.POST, instance=community)
        if form.is_valid():
            form.save()
            return render(request, 'join-community.html', {
                'community_name': community_name,
                'community': community,
                'user_joined': user_joined,
                'username': username,
                'posts': posts,
                'comments': comments,
            })  # Redirect to home page or wherever you want after editing rules
    else:
        form = EditRulesForm(instance=community)
    return render(request, 'edit-rules.html', {'form': form, 'community_name': community_name,
                                               'rules': community.rules})


def community(request, community_name):
    # Get username
    username = request.session.get('username')
    # Get communities user joined
    user_joined = UserCommunity.objects.filter(username=username, community_name=community_name).exists()
    # Get current community object
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
            'form': form
        })
    else:
        # If the user hasn't joined the community, redirect them to the home page or show an error message
        return redirect('home_page')


def post_view(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    comments = Comments.objects.all()
    return render(request, 'post.html', {'post': post, 'comments': comments })


def join_community(request, community_name):
    if request.method == 'POST':
        # Get current community
        community = get_object_or_404(Community, name=community_name)
        # Get posts of the current community
        posts = Posts.objects.filter(community_name=community_name)
        # Get comments for the current post
        comments = Comments.objects.all()
        # Get authenticated users' name
        username = request.session.get('username')
        # Get list of communities user joined.
        user_joined = UserCommunity.objects.filter(username=username, community_name=community_name).exists()
        if not user_joined:
            # User is not already a member of the community, add them and redirect to community page
            UserCommunity.objects.create(username=username, community_name=community_name)

        return render(request, 'join-community.html', {
                'community_name': community_name,
                'community': community,
                'user_joined': user_joined,
                'username': username,
                'posts': posts,
                'comments': comments
            })
    else:
        pass


def visit_community(request, community_name):
    # Get username
    username = request.session.get('username')
    # Get list of communities user joined
    user_joined = UserCommunity.objects.filter(username=username, community_name=community_name).exists()
    # Get current community object
    community = get_object_or_404(Community, name=community_name)
    # Get posts of the current community
    posts = Posts.objects.filter(community_name=community_name)
    # Get comments of the current post
    comments = Comments.objects.all()
    print("ID:" + str(posts[0].id))
    return render(request, 'join-community.html', {
        'community_name': community_name,
        'community': community,
        'user_joined': user_joined,
        'username': username,
        'posts': posts,
        'comments': comments,
    })


def follow_user(request, username):
    if request.method == 'POST':
        # Get username
        follower_username = request.session['username']
        # Create follower object
        follower_creation = UserFollower.objects.create(username=username, follower_username=follower_username)
        # Get user profile to display
        user_profile = UserProfile.objects.get(email=username)
        user_photo = "/media/" + str(user_profile.photo).split("'")[1]

        return render(request, 'follow-user.html', {'user_profile': user_profile, 'user_photo': user_photo})
    else:
        pass


def search_communities(request):
    q = request.GET.get('q')
    if q:
        communities = Community.objects.filter(name__icontains=q)
        registered_users = RegisteredUser.objects.filter(email__icontains = q)
        return render(request, 'search.html', {"users": registered_users, "communities": communities})
    else:
        return redirect('home')


def share_post(request, community_name):
    # Get username
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
        return redirect('community', community_name=community_name)
    else:
        form = TextBasedPostForm()

    return render(request, 'share-post.html', {'form': form})


def create_post_template(request, community_id):
    if request.method == 'POST':
        form = PostTemplateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            # Get selected fields and their mandatory status from the form data
            selected_fields = request.POST.getlist('fields')
            mandatory_fields = request.POST.getlist('mandatory_fields')

            # Combine selected fields and their mandatory status
            combined_fields = []
            for field, mandatory in zip(selected_fields, mandatory_fields):
                combined_fields.append(f"{field}:{mandatory}")

            fields_str = ','.join(combined_fields)

            # Save the template name and selected fields to the database
            template = PostTemplate.objects.create(template_name=name, community_id=community_id, fields=fields_str)
            template.save()

            return redirect('community_page')  # Redirect to community page after saving
        else:
            # Form is not valid, print errors for debugging
            print(f"Form errors: {form.errors}")
    else:
        form = PostTemplateForm()

    return render(request, 'create_post_template.html', {'form': form})