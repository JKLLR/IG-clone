from datetime import datetime
from django.shortcuts import  get_object_or_404, redirect, render
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib import messages
from .forms import SignUpForm,UpdateUserForm, UpdateUserProfileForm,PostForm,CommentForm
from .models import Profile, Post, User, Subscribers, Follow, Comment, Like
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages




def welcome(request):
    return render(request,'index.html')


def logoutUser(request):
	logout(request)
	return redirect('login')


def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post')
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))
            return redirect('login')
    else:
        return render(request, 'registration/login.html', {})

def register(request):
    if request.method == "POST":
        form =SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successful!"))
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration.html', {
        'form':form,
        })



@login_required(login_url='login')
def profile(request):
    # images = request.user.profile.posts.all()
    images = Post.objects.all()  
    print(images)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    contex = {
        'user_form': user_form,
        'prof_form': prof_form,
        'images': images,

    }
    return render(request, 'accounts_pages/profile.html', contex)

@login_required(login_url='login')
def user_profile(request,username):
    profile_user=get_object_or_404(User,username=username)
    if request.user == profile_user:
        return redirect('profile',username=request.user.username)
    user_posts=profile_user.profile.posts.all()

    followers=Follow.objects.filter(followed=profile_user.profile)  
    following=None
    for follower in followers:
        if request.user.profile == follower.follower:
            following=True  
        else:
            following=False
    context = {
        'profile_user':profile_user,
        'user_posts':user_posts,
        'followers':followers,
        'following':following
        }
    return render(request, 'accounts_pages/user_profile.html', context)
            
@login_required(login_url='login')
def post(request):
    images = Post.objects.all()
    print(images)
    comments = Comment.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit = False)
            image.user = request.user.profile
            image.save()
            messages.success(request, f'Successfully uploaded your pic!')
            return redirect('post')
    else:
        form = PostForm()
    return render(request, 'index.html', {"images":images[::-1], "form": form, "users": users, "comments": comments })


def image(request,image_id):
    try:
        image = Post.objects.get(id = image_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"image.html", {"image":image})

def new_comment(request,pk):
    post = Post.objects.get(pk = pk)
    comments = Comment.objects.all()
    if request.method == 'POST':

        form = CommentForm(request.POST)
        if form.is_valid():
            # name = request.user.username
            comment= form.cleaned_data['comment']
            obj = Comment(post = post,comment = comment,date = datetime.now())
            obj.save()
            print('object',obj)
        return redirect('post')
    else:
        form = CommentForm()
        print(form)

    return render(request, 'accounts_pages/comment.html', {"form": form,"comments":comments})
    
@login_required
def search_results(request):
    if 'profile' in request.GET and request.GET["profile"]:
        search_term = request.GET.get("profile")
        searched_profiles = Profile.search_profile(search_term)
        message = f"{search_term}"
        return render(request, 'accounts_pages/search.html', {"message":message,"profiles": searched_profiles})
    else:
        message = "You haven't searched for any profile"
    return render(request, 'accounts_pages/search.html', {'message': message})


def like(request,image_id):
    user = request.user
    post = Post.objects.get(id = image_id)
    current_likes = post.likes
    liked = Like.objects.filter(user = user,post = post).count()
    if not liked:
        Like.objects.create(user = user,post = post)
        current_likes = current_likes + 1
    else:
        Like.objects.filter(user = user,post = post).delete()  
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()

    return redirect('post')