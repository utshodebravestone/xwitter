from django.urls import path

from .views import feed_view, profiles_view, profile_view, login_view, logout_view

urlpatterns = [
    path('', feed_view, name='home'),
    path('feed/', feed_view, name='feed'),
    path('profiles/', profiles_view, name='profiles'),
    path('profile/<int:pk>', profile_view, name='profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
