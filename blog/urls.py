from django.urls import path
from . import views

urlpatterns = [
    path('', views.bloghome, name='blogHome'),
    path('<str:slug>', views.blogPost, name='blogPost')
]