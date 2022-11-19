from multiprocessing import context
import numbers
from unicodedata import name
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.template.defaulttags import register

from article.models import Article

from .forms import ArticleForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@register.filter
def index(request):
    context = {
        "Programing_Languge" : ['Python','PHP','Javascript','C++','C#'],
        "frameworks" : ['OOP','A lot of libs ','Flask' ,'Django', 'Bootstrap','PyQt5','SqlAlchemy','Tensorflow/Keras' ],

        "n" : 10
    }
    
    return render(request,'index.html',context)  

def about(request):
    return render(request,'about.html')

def articles(request):
    articles = Article.objects.all() 

    return render(request,'articles.html',{'articles':articles})



@login_required(login_url="user:loginUser")
def dashbord(request):
    articles = Article.objects.filter(author=request.user);
    context = {
        "articles":articles
    }
    for i in articles:
        print(i,'----')
    return render(request,"dashbord.html",context)


@login_required(login_url='user:loginUser')
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        print("Nathan ",request.POST)
        print("sky",request)
    if form.is_valid():

        article = form.save(commit=False)
        
        article.author = request.user
        article.save()

        messages.success(request,'Article created')
        return redirect('index')

    return render(request,'addarticle.html',{"form":form})

def detail(request,id):
    #print(id)
    #myarticle =  Article.objects.filter(id=id).first()
    myarticle= get_object_or_404(Article,id=id)
    #print(myarticle)
    context = {
        "myarticle":myarticle
    }
    print(myarticle.article_image)
    return render(request,'detail.html',context)

@login_required(login_url='user:loginUser')
def updateArticle(request,id):
    article = get_object_or_404(Article,id=id)
    form = ArticleForm(request.POST or None, request.FILES or None , instance= article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()

        messages.success(request,'Article updatet');
        return redirect('index')
    return render(request,'update.html',{'form':form})

@login_required(login_url='user:loginUser')
def deleteArticle(request,id):
    article = get_object_or_404(Article,id=id)
    article.delete()
    messages.success(request,'Article deleted')
    return redirect('article:dashbord')






@login_required(login_url=' user:loginUser')vsdavv

