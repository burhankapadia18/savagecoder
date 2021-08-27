from django.shortcuts import render, HttpResponse, redirect
from .models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.


def bloghome(request):
    allPost = Post.objects.all()
    context = {'allPost': allPost}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    repdict = {}
    for reply in replies:
        if reply.parent.sno not in repdict:
            repdict[reply.parent.sno] = [reply]
        else:
            repdict[reply.parent.sno].append(reply)
    # print(repdict)
    context = {'post': post, 'comments': comments, 'replies': repdict}
    return render(request, 'blog/blogpost.html', context)


def postComment(request):
    if request.method == 'POST':
        comment=request.POST.get('comment')
        user=request.user
        post_sno = request.POST.get('postSno')
        post= Post.objects.get(sno=post_sno)
        parentComment_sno = request.POST.get('parentSno')
        if parentComment_sno == "":
            comment = BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parentComment = BlogComment.objects.get(sno=parentComment_sno)
            comment = BlogComment(comment= comment, user=user, post=post, parent=parentComment)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
        return redirect(f"/blog/{post.slug}")
