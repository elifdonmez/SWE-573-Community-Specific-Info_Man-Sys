from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .forms import RegistrationForm, LoginForm
from .models import User

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
        user= User.objects.get(email=request.POST.getlist('email')[0])
        print(user.password)
        print(make_password(request.POST.getlist('password')[0]))
        if user is not None and check_password(request.POST.getlist('password')[0], user.password ):
            # Redirect to a success page
            return redirect('home')
        else:
            # Invalid login
            return render(request, 'login.html', {'error_message': 'Invalid email or password.'})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


