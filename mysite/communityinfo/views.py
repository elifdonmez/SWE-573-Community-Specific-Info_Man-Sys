from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .forms import RegistrationForm, LoginForm, CommunityCreationForm
from .models import Community, UserCommunity, RegisteredUser
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
    return render(request, 'home.html', {'communities': communities, 'username': username})


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
        print("User Name: " + username)
        print("Community Name: " + community_name)
        community_creation = UserCommunity.objects.create(username=username, community_name=community_name)
        community_creation.save()
        return redirect('home')
    else:
        # Handle the case when the request method is not POST
        # This can include displaying an error message or redirecting the user
        pass
