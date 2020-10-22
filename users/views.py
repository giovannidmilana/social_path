from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, ProfileForm, Post_, ProfilePhotoForm
from .models import *
#from .models import User_Post, Chat, Message
from django.db import models
from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import *
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import (
    LoginView,
)
import datetime


# Create your views here.

class login_view(LoginView):
    template_name = 'users/login.html'


def logout_view(request):
    """Log the user out."""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))



def register(request):
    """register new user"""
    if request.method != 'POST':
        user_form = UserForm()
    else:
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            authenticated_user = authenticate(username=new_user.username,password=request.POST['password1'])
            login(request, authenticated_user)            
            return HttpResponseRedirect(reverse('users:create_profile'))
            
    context = {'user_form': user_form}
    return render(request, 'users/register.html', context)


def create_profile(request):
    if request.method != 'POST':
        # show empty form
        profile_form = ProfileForm()
        profile_photo_form = ProfilePhotoForm()
    else:
        profile_photo_form = ProfilePhotoForm(request.POST, request.FILES)
        profile_form = ProfileForm(data=request.POST)
        if profile_form.is_valid() and profile_photo_form.is_valid():
            profile_photo = profile_photo_form.save(commit=False)
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile_photo.owner = request.user
            profile.profile_image = profile_photo
            profile.save()
            profile_photo.save()          
            return HttpResponseRedirect(reverse('users:disp_post'))
            
    context = {'profile_form': profile_form, 'photo_form' : profile_photo_form}
    return render(request, 'users/create_profile.html', context)


@login_required
def profile_edit_view(request):
    user = Profile.objects.get(user=request.user.id)
    if request.method != 'POST':
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = UserEditForm(instance=request.user)
     
    else:
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        user_form = UserEditForm(request.POST, instance=request.user)
        
        if profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('users:disp_post'))   

        
    context = {'profile_form': profile_form, 'user_form' : user_form, 'user' : user}
    return render(request, 'users/profile_edit.html', context)


def profiles_tm(request):
    """show all topics"""
    profiles_ = User.objects.all().select_related('profile')
    profile_photos = ProfilePhoto.objects.all()
    context = {'profiles_': profiles_, 'profile_photos' : profile_photos}
    return render(request, 'users/profiles_tm.html', context)

@login_required
def user_post(request):
    if request.method != 'POST':
        form = Post_()

    else:
        form = Post_(data=request.POST) 

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.date_added = datetime.datetime.now()
            new_post.save()
            print(new_post.id)
            return HttpResponseRedirect(reverse('users:disp_post'))

    context = {'form': form}
    return render(request, 'users/new_post.html', context)

@login_required
def disp_post(request):
    form = Post_()
    com_form = CommentForm()
    posts_ = []
    posts = User_Post.objects.all().order_by('-date_added')
    for post in posts.order_by('-date_added'):
        p = {'profile_photo' : ProfilePhoto.objects.get(owner=post.owner.id), 'post' : post, 'comments' : Comment.objects.filter(post=post.id)}
        posts_.append(p)
        
    context = {'posts_' : posts_, 'form' : form, 'com_form' : com_form}
    return render(request, 'users/posts1.html', context)




def post(request, post_id):
    post = User_Post.objects.get(id=post_id)
    comments = post.comment_set.order_by('-date_added')
    context = {'post': post, 'comments' : comments}
    return render(request, 'users/post.html', context)

@login_required
def new_comment(request, post_id):
    """ add a new entry for a particular topic."""
    post = User_Post.objects.get(id=post_id)
    if request.method != 'POST':
        # No data submitted: create a blank form.
        com_form = CommentForm()
    else:
        # POST data submitted: process data.
        com_form = CommentForm(data=request.POST)
        if com_form.is_valid():
            new_comment = com_form.save(commit=False)
            new_comment.post = post
            new_comment.owner = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse('users:disp_post'))
    context = {'post': post, 'com_form': com_form}
    return render(request, 'users/new_comment.html', context)

@login_required
def profile_user(request, user_id):
    posts_ = []
    posts = User_Post.objects.filter(owner=user_id)
    for post in posts.order_by('-date_added'):
        p = {'profile_photo' : ProfilePhoto.objects.get(owner=post.owner.id), 'post' : post, 'comments' : Comment.objects.filter(post=post.id)}
        posts_.append(p)
    chats = Chat.objects.filter(user1=request.user)
    chats_ = Chat.objects.filter(user2=request.user)
    chats__ = chats | chats_
    profile = User.objects.get(id=user_id)
    profile_ = Profile.objects.get(user=user_id)
    profile_photo = ProfilePhoto.objects.get(owner_id=user_id)
    context = {'profile_photo' : profile_photo, 'profile' : profile, 'profile_' : profile_, 'posts_' : posts_}
    return render(request, 'users/profile.html', context) 

@login_required
def edit_profile_photo(request):
    user = request.user
    profile = Profile.objects.get(pk=user.id)
    profile_photo_ = ProfilePhoto.objects.get(owner_id=user.id)

    if request.method != 'POST':
        profile_photo_form = ProfilePhotoForm(instance=request.user.profilephoto)

    else:
         profile_photo_form = ProfilePhotoForm(request.POST, request.FILES)
         
         if profile_photo_form.is_valid():
            profile_photo = profile_photo_form.save(commit=False)
            profile_photo.owner = request.user
            profile.profile_image = profile_photo
            profile.save()
            profile_photo.save()
            return HttpResponseRedirect(reverse('users:disp_post'))
    context = {'user' : user, 'profile_photo' : profile_photo_, 'profile_photo_form' : profile_photo_form, 'profile' : profile}
    return render(request, 'users/edit_profile.html', context)

@login_required
def delete_post(request, post_id):
    post = User_Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post_id)
    post.delete()
    for comment in comments:
        comment.delete()
    return HttpResponseRedirect(reverse('users:disp_post'))
    
@login_required   
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return HttpResponseRedirect(reverse('users:disp_post'))

@login_required
def messaging(request, user_id):
    user_1 = request.user
    user_2 = User.objects.get(id=user_id)
    now = datetime.datetime.now()
    if Chat.objects.filter(user1=user_1, user2=user_2):
        chat = Chat.objects.get(user1=user_1, user2=user_2)
    elif Chat.objects.filter(user2=user_1, user1=user_2):
        chat = Chat.objects.get(user2=user_1, user1=user_2)
    else:
        chat = Chat(user1=user_1, user2=user_2, created=now)
        chat.save()
    message_form = MessageForm()
    messages = Message.objects.filter(in_chat=chat)
    print(messages)
    context = {'messages' : messages, 'chat' : chat, 'user' : user_1, 'message_form' : message_form, 'user_id' : user_id}
    return render(request, 'users/chat.html', context)

@login_required
def send_message(request, chat_id, user_id):
    chat = Chat.objects.get(id=chat_id)
    if request.method != 'POST':
        message_form = MessageForm()
    else:
        # POST data submitted: process data.
        message_form = MessageForm(data=request.POST)
        #Chat.objects.filter(in_chat=chat, id=chat.id)
        if message_form.is_valid():
            #chat.save()
            print(chat)
            new_message = message_form.save(commit=False)
            new_message.in_chat = chat
            new_message.user = request.user
            new_message.save()
            return HttpResponseRedirect(reverse('users:messaging', args=[user_id]))
    
    
class SearchResultsView(ListView):
    model = User
    template_name = 'users/search_results.html'
    
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query) | Q(username__icontains=query))
        if ' ' in query:
            object_list = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query) | Q(username__icontains=query) | Q(last_name__icontains=query.split()[0]) | Q(last_name__icontains=query.split()[1]))
        return object_list
    

def testing():
    posts = User_Post.objects.all().order_by('date_added')
    comments = Comment.objects.all()
    tmp = []
    list_ = []
    for post in posts:
        if tmp:
            list_.append(tmp)
            tmp = []
        for comment in comments:
            if comment.post.id == post.id:
                tmp.append(comment)         
    return list_  

@login_required
def messages(request):
    chat2 = Chat.objects.filter(user1=request.user)
    chat1 = Chat.objects.filter(user2=request.user)
    chats = chat1 | chat2
    c = []
    for chat in chats:
        if Message.objects.filter(in_chat=chat):
            messages = Message.objects.filter(in_chat=chat)
            print(messages.reverse()[0])
            t = {'chat' : chat, 'message' : messages[0]}
            c.append(t)
    context = {'chats' : chats}
    return render(request, 'users/messages.html', context)

def testing2():
    posts = User_Post.objects.all()
    comment_list = []
    for post in posts:
        comments = post.comment_set.order_by('date_added')        
        comment_list.append(comments)
    return comment_list


#deletes all comments when called
def del_comments():
    comments = Comment.objects.all()
    for comment in comments:
        comment.delete()

#deletes all posts when called
def del_posts():
    posts = User_Post.objects.all()
    for post in posts:
        post.delete()

def del_profile_photos():
    photos = ProfilePhoto.objects.all()
    users = User.objects.all()
    profiles = Profile.objects.all()
    for photo in photos:        
        photo.owner = users[0]
        photo.owner_id = 74
        photo.delete()
    for user in users:        
        #.owner = users[0]
        #photo.owner_id = 74
        user.delete()
    for profile in profiles:        
        #.owner = users[0]
        #photo.owner_id = 74
        profile.delete()
        
def del_messages_chats():
    chats = Chat.objects.all()
    messages = Message.objects.all()
    for chat in chats:
        chat.delete()
    for message in messages:
        message.delete()
#del_comments()
#del_posts()
#del_profile_photos()
#del_messages_chats()
