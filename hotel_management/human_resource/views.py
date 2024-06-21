from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from .forms import MyUserCreationForm

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store:room_all')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('store:room_all')
        else:
            messages.error(request, 'Username OR password does not exit')
    return render(request, 'login_register/login.html')

def register(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('store:room_all')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'login_register/register.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('store:room_all')