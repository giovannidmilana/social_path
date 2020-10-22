from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
#from .managers import PersonManager
from django.db import models


from django.db.models.signals import post_save
from django.dispatch import receiver


class User_Post(models.Model):
    """A topic the user is learning about"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    post_text = models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
 
    def __str__(self):
        """Return a string representation of the model."""
        #print(self.text)
        return self.post_text


class ProfilePhoto(models.Model): 
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_image = models.ImageField(upload_to='images/') 

    def get_photo_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        else:
            return "images/users.png"



class Profile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_image = models.OneToOneField(ProfilePhoto, on_delete=models.CASCADE,)
    bilingual = models.BooleanField(default=False, null=True)





@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    #pass





class Comment(models.Model):
    """something specific learned about a topic"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #topic = models.ForeignKey(User_Post, on_delete=models.CASCADE)
    post = models.ForeignKey(
    User_Post,
    on_delete=models.CASCADE,
    )
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
        

    class Meta:
        verbose_name_plural = 'comments'

    def __str__(self):
        if len(self.text) >= 50:
            """Return a string represerntation of the model"""
            return self.text[:50] + "..."
        else:
             return self.text

class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats', null=True)
    created = models.DateTimeField(auto_now_add=True)

    def create(cls, user1, user2, created):
        chat = cls(user1=user1, user2=user2, created=created)
        # do something with the book
        return chat


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    in_chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500) # what length you want




