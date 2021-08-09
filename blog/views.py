from django.shortcuts import render, HttpResponse, redirect
from .models import Post, BlogComment
from django.contrib import messages

# Create your views here.


def bloghome(request):
    allPost = Post.objects.all()
    context = {'allPost': allPost}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post)
    context = {'post': post, 'comments': comments}
    return render(request, 'blog/blogpost.html', context)


def postComment(request):
    if request.method == 'POST':
        comment=request.POST.get('comment')
        user=request.user
        post_sno =request.POST.get('post_sno')
        post= Post.objects.get(sno=post_sno)
        comment=BlogComment(comment= comment, user=user, post=post)
        comment.save()
        messages.success(request, "Your comment has been posted successfully")
        
        return redirect(f"/blog/{post.slug}")
