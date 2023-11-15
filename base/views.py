from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.response import Http404

from .models import Profile


def home_view(request):
    return render(request, 'base/home.html', {})


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

        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'follow':
                request.user.profile.follows.add(profile)
            elif action == 'unfollow':
                request.user.profile.follows.remove(profile)
            request.user.profile.save()

        return render(request, 'base/profile.html', {'profile': profile})
    else:
        messages.error(
            request, "you can't access profile page unless you are logged in")
        return redirect('/admin/login')
