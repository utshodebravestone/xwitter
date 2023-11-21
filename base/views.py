from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count

from .models import Profile, Tweet, User
from .forms import TweetForm, RegisterForm, ProfilePictureForm


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

        tweets = Tweet.objects.filter(
            user__profile__followed_by=request.user.profile).order_by('-created_at')
        return render(request, 'base/feed.html', {'tweets': tweets, 'form': form})
    else:
        messages.warning(
            request, "you can't access your feeds unless you are logged in")
        return redirect('login')


def profiles_view(request):
    if request.user.is_authenticated:
        # profiles = Profile.objects.exclude(user=request.user).order_by('followed_by')
        name = request.GET.get('name')
        profiles = Profile.objects.annotate(
            follower_count=Count('followed_by')).order_by('-follower_count')
        if name:
            profiles = profiles.filter(user__username__startswith=name)
        return render(request, 'base/profiles.html', {'profiles': profiles})
    else:
        messages.warning(
            request, "you can't explore other's profile unless you are logged in")
        return redirect('login')


def profile_view(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by('-created_at')

        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'follow':
                request.user.profile.follows.add(profile)
                messages.success(
                    request, f"you followed @{profile.user.username}")
            elif action == 'unfollow':
                request.user.profile.follows.remove(profile)
                messages.success(
                    request, f"you unfollowed @{profile.user.username}")
            request.user.profile.save()
            return redirect(f'/profile/{pk}')

        return render(request, 'base/profile.html', {'profile': profile, 'tweets': tweets})
    else:
        messages.warning(
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
            messages.warning(
                request, "credentials are incorrect")
    return render(request, 'base/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            logout(request)
            return redirect('login')
        return render(request, 'base/logout.html')
    else:
        messages.warning(
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
            messages.warning(
                request, "got invalid data")
    return render(request, 'base/register.html', {'form': form})


def profile_update_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        user_form = RegisterForm(request.POST or None,
                                 request.FILES or None, instance=user)
        profile_form = ProfilePictureForm(
            request.POST or None, request.FILES or None, instance=profile)
        if request.method == 'POST':
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(
                    request, "profile updated successfully")
                login(request, user)
                return redirect(f'/profile/{user.pk}')
            else:
                messages.warning(
                    request, "got invalid data")
        return render(request, 'base/update_profile.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.warning(
            request, "you can't access profile page unless you are logged in")
        return redirect('login')


def like_view(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        messages.success(request, 'liked successfully')
        return redirect('feed')
    else:
        messages.warning(
            request, "you can't access profile page unless you are logged in")
        return redirect('login')


def tweet_view(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        return render(request, 'base/tweet.html', {'tweet': tweet})
    else:
        messages.warning(
            request, "you can't access tweet page unless you are logged in")
        return redirect('login')
