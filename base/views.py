from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Profile, Tweet


def feed_view(request):
    if request.user.is_authenticated:
        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, 'base/feed.html', {'tweets': tweets})
    else:
        messages.error(
            request, "you can't access feed page unless you are logged in")
        return redirect('/admin/login')


def profiles_view(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'base/profiles.html', {'profiles': profiles})
    else:
        messages.error(
            request, "you can't access profile page unless you are logged in")
        return redirect('/admin/login')


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
        return redirect('/admin/login')


def tweet_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            text = request.POST.get('tweet')
            tweet = Tweet(text=text, user=request.user)
            tweet.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.error(
            request, "you can't access profile page unless you are logged in")
        return redirect('/admin/login')
