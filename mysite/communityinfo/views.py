from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .forms import RegistrationForm, LoginForm, CommunityCreationForm
from .models import User, Community, UserCommunity

def register(request):
    if request.method == 'POST':
        user = User.objects.create(email=request.POST.getlist('email')[0], password=make_password(request.POST.getlist('password')[0]))
        user.save()
        return redirect('login')  # Redirect to a success page
    else:
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        # ToDo: Workaround since the Django Authenticator is not working right now
        user= User.objects.get(email=request.POST.getlist('email')[0])
        if user is not None and check_password(request.POST.getlist('password')[0], user.password ):
            # Redirect to a success page
            return redirect('home_page')
        else:
            # Invalid login
            return render(request, 'login.html', {'error_message': 'Invalid email or password.'})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def home_page(request):
    communities = Community.objects.all()
    return render(request, 'home.html', {'communities': communities})


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
        # Query the Community model to retrieve the corresponding community object based on the community name
        community = Community.objects.get(name=community_name)

        # Obtain the community ID from the retrieved community object
        current_community_id = community.id
        # TODO: Get user id and fix it
        current_user_id = 2
        # Create a Community_Creation object
        community_creation = UserCommunity.objects.create(user_id=current_user_id, community_id=current_community_id)
        community_creation.save()
        # Optionally, you can redirect the user to a different page after joining the community
        return redirect('home')
    else:
        # Handle the case when the request method is not POST
        # This can include displaying an error message or redirecting the user
        pass
