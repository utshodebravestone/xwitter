from django import forms

from .models import Tweet


class TweetForm(forms.ModelForm):
    text = forms.CharField(max_length=200, required=True, widget=forms.widgets.Textarea(
        attrs={'placeholder': 'type what you wanna xweet about...'}
    ), label='')

    class Meta:
        model = Tweet
        exclude = ('user',)
