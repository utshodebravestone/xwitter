from django.urls import path

from .views import home_view, profiles_view, profile_view

urlpatterns = [
    path('', home_view, name='home'),
    path('profiles/', profiles_view, name='profiles'),
    path('profile/<int:pk>', profile_view, name='profile'),
]
