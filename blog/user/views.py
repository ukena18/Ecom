# use redirect function to change html 
from django.shortcuts import render, redirect
from . import forms
# almoste the same form importing
from .forms import LoginForm
import user
# add user model for create new user
from django.contrib.auth.models import User
# add login for login the registred user emideatly
from django.contrib.auth import login,authenticate,logout

from django.contrib import messages

#-----------------------------
# Create your views here.
def register(request):
    form = forms.RegisterForm(request.POST or None);
    
        # first fill your form with post data;
        #form = forms.RegisterForm(request.POST or None);
        # to start clean method use 
    if form.is_valid():
        #thats mean in form adata evfy thing is ok
        username = form.cleaned_data.get('username');
        password = form.cleaned_data.get('password');
            
        newUser = User(username=username)
        newUser.set_password(password)
        newUser.save()
            
        print(login(request,newUser))
            #add message
        messages.info(request,'You secsessfuly registretred');

        return redirect('index')
    context = {
        "form" : form
    }
    return render(request,'register.html',context)
 


def loginUser(request):
    form = LoginForm(request.POST or None)
    context= {
        "form": form,
    }
    print(request)
    if form.is_valid():
        username = form.cleaned_data.get('username');
        password = form.cleaned_data.get("password");
        print(username,password)
        user_in= authenticate(username=username,password=password);
        print(user_in)
        if user_in is None:
            messages.info(request,'Login or password is invalid')
            return render(request,'login.html',context)
        messages.success(request,'You secsessfuly entred')
        print(request)
        lg = login(request,user_in)
        print(lg)
        if user_in.is_active:
            print('active')

        return redirect('index')

    return render(request,'login.html',context)


def logOut(request):
    logout(request)
    messages.success(request,'Secsessfuly log out')
    return redirect('index')

