# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from TIL_App.models import Post
from django.shortcuts import render, redirect
from django.utils import timezone
import praw, random
from forms import LoginForm

# a function that takes the Reddit thread title and returns a presentable string
def clean_title(title):
    arr = title.split(' ')
    if arr[0].upper() in ['TIL', 'TIL:', 'TIL,', 'TIL;', 'TIL-', 'TIL--']:
        arr.pop(0)
    if arr[0].lower() == 'i' and arr[1].lower() == 'learned':
        arr = arr[2:]
    if arr[0] in ['-', ':']:
        arr.pop(0)
    if arr[0].lower() in ['that', 'that,']:
        arr.pop(0)
    arr[0] = arr[0].capitalize()
    if arr[0][0] in ['"', "'"]:
        arr[0] = arr[0][0] + arr[0][1:].capitalize()
    if arr[-1][-1] == '.':
        arr[-1] = arr[-1][:-1]
    return ' '.join(arr)

# a function that checks whether a post satisfies rule VI of the TIL subreddit
def is_valid_title(title):  
    new_title = clean_title(title)
    if new_title.split(' ')[0].lower() in ['of', 'about', 'how']:
        return None
    return new_title


# a function that returns a list of the the first posts in the TIL subreddit
def list_posts(num_posts, client_id, client_secret):
    reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='my user agent')

    return list(reddit.subreddit('todayilearned').hot(limit=num_posts))


# check if the data has been updated since the last update
# default is set to one minute for testing purposes
def need_update(days=0, hours=0, minutes=1):
    prev_update = timezone.now() - timezone.timedelta(days=days, hours=hours, minutes=minutes)
    if Post.objects.exists() and Post.objects.filter(created__gte=prev_update).exists():        
        return False
    return True 


# get a list of posts from reddit
def get_list_from_reddit(num_posts, client_id, client_secret):  
    reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='my user agent')
        
    posts = list(reddit.subreddit('todayilearned').hot(limit=num_posts))    
    random.shuffle(posts)
    return posts


# update the database if enough time has elapsed
def populate_database(num_posts, client_id, client_secret):
    if not need_update():
        return 
    
    Post.objects.all().delete()    
    list_posts = get_list_from_reddit(num_posts, client_id, client_secret)
    for post in list_posts:       
        clean_post_title = is_valid_title(post.title)  
        if not clean_post_title:
            continue               
        post_url = 'http://www.reddit.com' + post.permalink
        external_url = post.url
        post = Post(title=clean_post_title, external_url=external_url, post_url=post_url)
        post.save()
           

# get a random pk from the db
def get_random_pk():
    first_pk = int(Post.objects.first().pk) 
    last_pk = int(Post.objects.last().pk)     
    return random.randint(first_pk, last_pk)


# functions for the various html pages
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            client_id = form.cleaned_data['client_id']
            client_secret = form.cleaned_data['client_secret']
            num_posts = form.cleaned_data['num_posts']
            populate_database(num_posts, client_id, client_secret)
            return redirect('TIL:welcome')
    else:
        form = LoginForm()
        return render(request, 'TIL_App/TIL_login.html', context={'form': form})

def welcome_page(request):
    curr_pk = get_random_pk()
    return render(request, 'TIL_App/TIL_welcome.html', context={'curr_pk': curr_pk})

def about_page(request):
    return render(request, 'TIL_App/TIL_about.html', context={})

def tell_me(request, pk):
    curr_post = Post.objects.get(pk=pk)
    next_pk = get_random_pk()    
    return render(request, 'TIL_App/TIL_smthng_new.html', context={'post': curr_post, 'next_pk': next_pk })

