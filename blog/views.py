from django.shortcuts import render, HttpResponse
from .models import Post

# Create your views here.

def bloghome(request):
    allPost = Post.objects.all()
    context = {'allPost': allPost}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    print(post)
    context = {'post': post}
    return render(request, 'blog/blogpost.html', context)
