from django import forms
from django.contrib.auth.models import User
from . models import Profiles, Comment, Message


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class ProfilesForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ('nickname', 'image')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('message',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

