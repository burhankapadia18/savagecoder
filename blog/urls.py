from django.urls import path
from . import views

urlpatterns = [
    path('', views.bloghome, name='blogHome'),
    # API to post a comment
    path('postComment', views.postComment, name='postComment'),
    path('<str:slug>', views.blogPost, name='blogPost'),
    
]