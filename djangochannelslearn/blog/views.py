from django.shortcuts import render, HttpResponse
from .models import Blog
import datetime
# Create your views here.


def index(request):
    return render(request, 'blog/index.html')


def tweet(request):
    d = datetime.time(10, 33, 45)
    blog = Blog.objects.create(post="SOME shiit in database")
    blog.save()
    return HttpResponse("sdsds")