from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import requests
from bs4 import BeautifulSoup as bs
from .models import Github 

def index(request):
    if request.method == 'POST':
        github_user = request.POST['github_user']
        user = request.POST['user']
        url = 'https://github.com/'+github_user
        r = requests.get(url)
        soup = bs(r.content)
        profile = soup.find('img', {'alt': 'Avatar'})['src']
        
        new_github = Github(
            githubuser = github_user,
            imagelink = profile,
            username = user
        )

        new_github.save()
        messages.info(request, 'User Image Saved')
        return redirect('/')

    context = {}
    return render(request, 'index.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords dont match')
            return redirect('register')
        return redirect('/')     
    else:
        context = {}
        return render(request, 'signup.html', context)
    
def login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        context = {}
        return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('login')

def images(request):
    gh = Github.objects.filter(username=request.user.username)
    
    
    
    context = {'gh':gh}
    return render(request, 'images.html', context)



