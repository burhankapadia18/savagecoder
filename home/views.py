from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home/home.html')


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(phone)<10 or len(email)<3 or len(content)<4:
            messages.error(request, 'Please fill the form correctly')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your query has been sent successfully')
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query)<2 or len(query)>70:
        messages.warning(request, 'Please enter valid keyword')
        return render(request,'home/home.html')
    allPost1 = Post.objects.filter(title__icontains=query)
    allPost2 = Post.objects.filter(content__icontains=query)
    allPost = allPost1.union(allPost2)
    if len(allPost) == 0:
        messages.warning(request, 'sorry! there are no blogs related to your search')
        return redirect('home')
    params = {'allPost': allPost, 'query': query}
    messages.success(request, f'found {len(allPost)} blog(s) related to your search')
    return render(request, 'home/search.html', params)


def signUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if fname=="" or lname=="" or username=="":
            messages.warning(request, 'Please fill proper details')
            return render(request,'home/signup.html')
        if pass1!=pass2:
            messages.error(request, "Password doesn't match")
            return render(request,'home/signup.html')
        
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your SavageCoder account has been created successfully!')
        return redirect('home')
    else:   
        return render(request,'home/signup.html')
