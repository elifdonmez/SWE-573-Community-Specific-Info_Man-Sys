from django import forms
from django.contrib.auth import authenticate
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from .forms import RegistrationForm, LoginForm, CommunityCreationForm, EditRulesForm, TextBasedPostForm, ProfileForm, \
    PostTemplateForm, CustomTemplatePostForm, AdvancedSearchForm
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
        if user_profile:
            print("OK")
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
            if user is not None and check_password(request.POST.getlist('password')[0], user.password):
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
                                         'posts': posts, 'user_communities': user_communities,
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
            is_private = request.POST.getlist('privacy')[0] == 'on'
        else:
            is_private = False
        # create community object
        community = Community.objects.create(name=request.POST.getlist('name')[0],
                                             description=request.POST.getlist('description')[0],
                                             privacy=is_private,
                                             rules=request.POST.getlist('rules')[0],
                                             creator=username)
        # community.save()
        form = CommunityCreationForm()
        UserCommunity.objects.create(username=username, community_name=community.name)
        template_name = "default template"
        community_id = Community.objects.filter(name=community.name)
        fields = "description:1:non_mandatory:Description"
        is_active = 1
        default_template = PostTemplate.objects.create(template_name=template_name, community_id=community_id[0].id,
                                                       fields=fields, is_active=is_active)
        default_template.save()
        return render(request, 'home.html',
                      {'form': form, 'communities': communities, 'people': people, 'username': username,
                       'posts': posts, 'user_communities': user_communities})
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
    return render(request, 'post.html', {'post': post, 'comments': comments})


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
        registered_users = RegisteredUser.objects.filter(email__icontains=q)
        return render(request, 'search.html', {"users": registered_users, "communities": communities})
    else:
        return redirect('home')


def share_post(request, community_name):
    username = request.session.get('username')
    community = Community.objects.get(name=community_name)
    templates = PostTemplate.objects.filter(community_id=community.id)

    if request.method == 'POST':
        template_id = request.POST.get('template')

        print("template id " + str(template_id))

        if template_id:
            selected_template = PostTemplate.objects.get(pk=template_id)
            form = CustomTemplatePostForm(request.POST, template=selected_template)
        else:
            new_post = Posts.objects.create(
                community_name=community_name,
                submitter_name=username,
                header=request.POST.get('header'),
                description=request.POST.get('description'),
                image_url=request.POST.get('image_url'),
                video_url=request.POST.get('video_url'),
                geolocation=request.POST.get('geolocation'),
                date_time_field=request.POST.get('date_time_field'),
                audio_url=request.POST.get('audio_url'),
                number_of_upvotes=0,
                number_of_downvotes=0,
                number_of_smiles=0,
                number_of_hearts=0,
                number_of_sadfaces=0,
                template_id=request.POST.get('template_id')
            )
            return redirect('community', community_name=community_name)

    else:
        default_template_id = PostTemplate.objects.filter(template_name="default template",
                                                          community_id=community.id)[0].id
        selected_template = PostTemplate.objects.get(pk=default_template_id)
        form = CustomTemplatePostForm(request.POST, template=selected_template)
        # Handle GET request to render initial form

    return render(request, 'share-post.html', {'form': form, 'templates': templates})


def advanced_search(request, community_name):
    community = Community.objects.get(name=community_name)
    templates = PostTemplate.objects.filter(community_id=community.id)

    if request.method == 'POST':
        template_id = request.POST.get('template')
        if template_id:
            return redirect('advanced_search_form', community_name=community_name, template_id=template_id)
        else:
            return redirect('community', community_name=community_name)
    else:
        return render(request, 'advanced-search.html', {'community_name': community_name, 'templates': templates})


def search_communities(request):
    q = request.GET.get('q')
    if q:
        communities = Community.objects.filter(name__icontains=q)
        registered_users = RegisteredUser.objects.filter(email__icontains=q)
        return render(request, 'search.html', {"users": registered_users, "communities": communities})
    else:
        return redirect('home')


def advanced_search_form(request, community_name, template_id):
    selected_template = PostTemplate.objects.get(pk=template_id)
    print("Request Method:", request.method)
    if request.method == 'POST':
        print("Hey Hey")
        form = AdvancedSearchForm(request.POST, template=selected_template)
        if form.is_valid():
            print("Form is valid")
            # Collect form data
            header = form.cleaned_data.get('header')
            description = form.cleaned_data.get('description')
            geolocation = form.cleaned_data.get('geolocation')
            date_time_field = form.cleaned_data.get('date_time_field')

            # Build the query based on provided inputs
            query = {}
            if header:
                query['header__icontains'] = header
            if description:
                query['description__icontains'] = description
            if geolocation:
                query['geolocation__icontains'] = geolocation
            if date_time_field:
                query['date_time_field'] = date_time_field
            query['template_id__icontains'] = template_id

            # Perform the search
            posts = Posts.objects.filter(template_id=template_id, **query)
            return render(request, 'advanced-search-results.html', {'posts': posts})
            return redirect('advanced_search_results', community_name=community_name)
    else:
        form = AdvancedSearchForm(template=selected_template)

    return render(request, 'advanced-search-form.html',
                  {'community_name': community_name, 'selected_template': selected_template, 'form': form})


def advanced_search_results(request, community_name):
    # Handle search results display here
    return render(request, 'advanced-search-results.html')


def create_post_template(request, community_id):
    community_name = Community.objects.filter(id=community_id)[0].name
    username = request.session.get('username')
    # Get list of communities user joined
    user_joined = UserCommunity.objects.filter(username=username, community_name=community_name).exists()
    # Get current community object
    # Get posts of the current community
    posts = Posts.objects.filter(community_name=community_name)
    # Get comments of the current post
    comments = Comments.objects.all()
    if request.method == 'POST':
        form = PostTemplateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            # Get selected fields and their mandatory status from the form data
            selected_fields = request.POST.getlist('fields')
            mandatory_fields = request.POST.getlist('mandatory_fields')
            custom_labels = request.POST.getlist('custom_labels')

            # Combine selected fields and their mandatory status
            combined_fields = []
            for field, mandatory, label in zip(selected_fields, mandatory_fields, custom_labels):
                combined_fields.append(f"{field}:{mandatory}:{label}")

            fields_str = ','.join(combined_fields)
            # Save the template name and selected fields to the database
            template = PostTemplate.objects.create(template_name=name, community_id=community_id, fields=fields_str)
            template.save()
            return redirect('visit_community', community_name=community_name)
        else:
            # Form is not valid, print errors for debugging
            print(f"Form errors: {form.errors}")
    else:
        form = PostTemplateForm()

    return render(request, 'create_post_template.html', {'form': form})