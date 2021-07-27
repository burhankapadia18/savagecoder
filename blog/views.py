from django.shortcuts import render, HttpResponse

# Create your views here.

def bloghome(request):
    return render(request, 'blog/blogHome.html')


def blogPost(request, slug):
    return render(request, 'blog/blogpost.html')
