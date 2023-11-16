from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count

from .models import Profile, Tweet
from .forms import TweetForm, RegisterForm


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
        # profiles = Profile.objects.exclude(user=request.user).order_by('followed_by')
        profiles = Profile.objects.annotate(
            follower_count=Count('followed_by')).order_by('-follower_count')
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
                messages.success(
                    request, f"you followed {profile.user.username}")
            elif action == 'unfollow':
                request.user.profile.follows.remove(profile)
                messages.success(
                    request, f"you unfollowed {profile.user.username}")
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
            return redirect('login')
        return render(request, 'base/logout.html')
    else:
        messages.error(
            request, "you can't access logout page unless you are logged in")
        return redirect('login')


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user=user)
            messages.success(
                request, "registered successfully")
            return redirect(f'/profile/{user.pk}')
        else:
            messages.error(
                request, "got invalid data")
    return render(request, 'base/register.html', {'form': form})
