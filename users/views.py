from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Message
from .forms import RegisterUserForm, ProfileForm, MessageForm
from .alerts import *
from .utils import searchProfiles, paginateProfiles

# Create your views here.
def profiles(request):
    # profiles = Profile.objects.all()
    # search_query = ''
    profiles, search_query = searchProfiles(request)
    custom_rage, profiles = paginateProfiles(request, profiles, 3)

    context = {'profiles': profiles, 'search_query': search_query, 'custom_rage': custom_rage}
    return render(request, 'users/profiles.html', context)


def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile}
    return render(request, 'users/profile.html', context)


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
    return render(request, 'users/profile-form.html', context)


def userLogin(request):
    if request.user.is_authenticated:
        return redirect('posts')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, loginSuccess)
            return redirect(request.GET['next'] if 'next' in request.GET else 'posts')
        else:
            messages.error(request, loginError)

    return render(request,'users/login.html')


def userRegister(request):
    if request.user.is_authenticated:
        return redirect('posts')

    form = RegisterUserForm()

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, registerSuccess)

            login(request, user)
            return redirect('edit-profile')
        else:
            messages.error(request, registerError)

    context = {'form': form}

    return render(request,'users/register.html', context)


@login_required(login_url='login')
def userLogoutPage(request):
    return render(request, 'users/logout.html')


@login_required(login_url='login')
def userLogout(request):
    logout(request)
    messages.success(request, logoutSuccess)
    return redirect('login')


@login_required(login_url='login')
def messagesView(request):
    profile = request.user.profile
    messages_obj = profile.messages.all()
    unread_count = messages_obj.filter(is_read=False).count()
    context = {'messages_obj': messages_obj, 'unread_count': unread_count}
    return render(request, 'users/messages-view.html', context)


@login_required(login_url='login')
def messageView(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message-view.html', context)


def createMessage(request, pk):
    receiver = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.receiver = receiver

            if sender:
                message.sender_2 = sender.user.first_name + " " + sender.user.last_name

            message.save()

            messages.success(request, 'Udało się wysłać wiadomość do ' + receiver.user.first_name + " " + receiver.user.last_name + ".")

            return redirect('profile', pk=receiver.id)
    context = {'receiver': receiver, 'form': form}
    return render(request, 'users/message-form.html', context)
