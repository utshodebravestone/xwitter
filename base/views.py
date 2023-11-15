from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Profile, Tweet
from .forms import TweetForm


def feed_view(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(
                    request, "xweeted successfully")
                return redirect('feed')

        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, 'base/feed.html', {'tweets': tweets, 'form': form})
    else:
        messages.error(
            request, "you can't access feed page unless you are logged in")
        return redirect('login')


def profiles_view(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'base/profiles.html', {'profiles': profiles})
    else:
        messages.error(
            request, "you can't access profile page unless you are logged in")
        return redirect('login')


def profile_view(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by('-created_at')

        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'follow':
                request.user.profile.follows.add(profile)
            elif action == 'unfollow':
                request.user.profile.follows.remove(profile)
            request.user.profile.save()

        return render(request, 'base/profile.html', {'profile': profile, 'tweets': tweets})
    else:
        messages.error(
            request, "you can't access profile page unless you are logged in")
        return redirect('login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(
                request, "logged in successfully")
            return redirect('feed')
        else:
            messages.error(
                request, "credentials are incorrect")
    return render(request, 'base/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            logout(request)
            return redirect('feed')
        return render(request, 'base/logout.html')
    else:
        messages.error(
            request, "you can't access logout page unless you are logged in")
        return redirect('login')
