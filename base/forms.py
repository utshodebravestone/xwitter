from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Tweet, Profile, User


class TweetForm(forms.ModelForm):
    text = forms.CharField(max_length=200, required=True, widget=forms.widgets.Textarea(
        attrs={'placeholder': 'type what you wanna xweet about...'}
    ), label='')

    class Meta:
        model = Tweet
        exclude = ('user',)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'your email'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'your username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''

        self.fields['password1'].widget.attrs['placeholder'] = 'your password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['placeholder'] = 'confirm your password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''


class ProfilePictureForm(forms.ModelForm):
    image = forms.ImageField(label='')

    class Meta:
        model = Profile
        fields = ('image',)
