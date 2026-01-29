from django import forms
from .models import Tweet, Profile,TweetImage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text']

class TweetImageForm(forms.ModelForm):
    class Meta:
        model = TweetImage
        fields = ['image']


class UserRegistration(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'job_title', 'department', 'team', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write something about yourself...'}),
        }
