"""defiune url pattterns for learning_logs"""

#from django.conf.urls  import url
from django.urls import path
from . import views
#from django.urls import include
app_name = 'learning_logs'

urlpatterns = [
    # Home page
    #THE PROPOSED WAY TO DO IN BOOK: url(r'^$', views.index, name='index'),
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    #(it appears i ca either use above format or the ladder)
    path('', views.topics, name='topics'),
    #path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    #path('index/<int:user_id>/', views.profile_user, name='profile_user'),

]
