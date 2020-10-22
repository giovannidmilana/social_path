
from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
#from .managers import PersonManager
from django.db import models
from .models import Profile, User_Post
from .models import *

class MessageForm(forms.ModelForm):
    text = forms.CharField(label='Message', max_length=500,
        widget=forms.Textarea(attrs={'rows':'3', 'cols': '100'}))
    class Meta:
        model = Message
        fields = ('text',)



class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2') 

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username') 



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio','bilingual',)



  
class ProfilePhotoForm(forms.ModelForm): 
  
    class Meta: 
        model = ProfilePhoto 
        fields = ['profile_image',] 


class Post_(forms.ModelForm):
    post_text = forms.CharField(label='New Post:', max_length=500,
        widget=forms.Textarea(attrs={'rows':'3', 'cols': '80'}))
    class Meta:
        model = User_Post
        fields = ('post_text',)
        

 

class CommentForm(forms.ModelForm):
    text = forms.CharField(label='', max_length=500,
        widget=forms.Textarea(attrs={'rows':'1', 'cols': '50'}))
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ''}
        

'''
class ChatForm(forms.ModelForm):
    class Meta:
         model = Chat
         fields = ['participants']
'''
