from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.

# html pages
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == 'POST':
        # get all the entries
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        # check for any false entry
        if len(name)<2 or len(phone)<10 or len(email)<3 or len(content)<4:
            messages.error(request, 'Please fill the form correctly')
        else:
            # create object and save to database
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your query has been sent successfully')
    return render(request, 'home/contact.html')

def search(request):
    # get the search query
    query = request.GET['query']
    # check for false/random query
    if len(query)<2 or len(query)>70:
        messages.warning(request, 'Please enter valid keyword')
        return render(request,'home/home.html')
    # get the posts matching the query
    allPost1 = Post.objects.filter(title__icontains=query)
    allPost2 = Post.objects.filter(content__icontains=query)
    allPost = allPost1.union(allPost2)
    # check if we found any blog
    if len(allPost) == 0:
        messages.warning(request, 'sorry! there are no blogs related to your search')
        return redirect('home')
    params = {'allPost': allPost, 'query': query}
    messages.success(request, f'found {len(allPost)} blog(s) related to your search')
    return render(request, 'home/search.html', params)

# Authentication API's
def signUp(request):
    if request.method == 'POST':
        # get the entries
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # check for false entries
        if len(username)>10:    # username must be under 10 characters
            messages.error(request, "Username must be under 10 characters")
            return redirect('signUp')
        if not username.isalnum():  # username should be alphanumeric
            messages.error(request, "Username should only contains letters and numbers")
            return redirect('signUp')
        if pass1!=pass2:    # passwords should be same
            messages.error(request, "Passwords do not match")
            return redirect('signUp')
        if len(pass1)<8:    # password length should be greater than 7
            messages.error(request, "Password length must be greater than 7")
            return redirect('signUp')
        # create the user and save to database
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your SavageCoder account has been created successfully!')
        return redirect('home')
    else:   
        return render(request,'home/signup.html')

def handleLogin(request):
    if request.method == 'POST':
        # get the username and password
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request, "Successfully Logged In")
            # return redirect('home')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Invalid Username or Password")
            # return redirect('home')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   # redirects to the page where it has been made to logout
