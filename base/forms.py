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

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = """<div id="emailHelp" class="form-text">Must be greater than 3 characters</div>"""

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label = ''
        self.fields[
            'email'].help_text = """<div id="emailHelp" class="form-text">Example: username@gmail.com</div>"""

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = """<div id="emailHelp" class="form-text">Must be greater than 6 characters and must not include your username or any common passwords (i.e: 123456, asdf etc.)</div>"""

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = """<div id="emailHelp" class="form-text">Same as the previous one</div>"""


class ProfilePictureForm(forms.ModelForm):
    image = forms.ImageField(label='')

    class Meta:
        model = Profile
        fields = ('image',)
