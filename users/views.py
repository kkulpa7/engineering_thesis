from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import RegisterUserForm, ProfileForm

# Create your views here.
def profiles(request):
    return render(request, 'users/profiles.html')


def profile(request):
    return render(request, 'users/profile.html')


@login_required(login_url='login')
def userProfile(request):
    profile = request.user.profile

    context = {'profile': profile}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('posts')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


def userLogin(request):
    if request.user.is_authenticated:
        return redirect('posts')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Udało się zalogować!')
            return redirect('posts')
        else:
            messages.error(request, 'Login lub hasło jest nieprawidłowe!')

    return render(request,'users/login.html')


def userRegister(request):
    if request.user.is_authenticated:
        return redirect('posts')

    form = RegisterUserForm()

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        print('POST')
        if form.is_valid():
            print('POST2')
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'Konto zostało utworzone!')

            login(request, user)
            return redirect('edit-profile')
        else:
            messages.error(request, 'Nie udało się utworzyć nowego konta!')

    context = {'form': form}

    return render(request,'users/register.html', context)


@login_required(login_url='login')
def userLogoutPage(request):
    return render(request, 'users/logout.html')


@login_required(login_url='login')
def userLogout(request):
    logout(request)
    messages.error(request, 'User was logout')
    # return render(request,'users/logout.html')
    return redirect('login')
