from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Tweet

admin.site.unregister(Group)
admin.site.unregister(User)


class InlinedProfile(admin.StackedInline):
    model = Profile


class CustomizedUser(admin.ModelAdmin):
    model = User
    fields = ['username', 'email']
    inlines = [InlinedProfile]


admin.site.register(User, CustomizedUser)
admin.site.register(Tweet)
