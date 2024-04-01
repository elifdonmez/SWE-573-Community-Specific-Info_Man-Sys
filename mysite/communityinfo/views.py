from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import RegistrationForm
from .models import User

def register(request):
    if request.method == 'POST':
        user = User.objects.create(email=request.POST.getlist('email')[0], password=make_password(request.POST.getlist('password')[0]))
        user.save()
        return redirect('registration_success')  # Redirect to a success page

    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})
