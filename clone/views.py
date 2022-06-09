from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Post, UserProfile, Comment
from django.contrib.auth.models import User
from .forms import CommentForm, PostForm, SignUpForm, UserProfileForm
from django.contrib import messages


@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    print(current_user)
    current_profile = UserProfileForm.objects.get(user_id=current_user.id)
    # current_profile=get_object_or_404(User,username=username)
    posts = Post.objects.all()
    comments = Comment.objects.all()

    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid():
            post = post_form.save(commit=False)

            post.profile = current_user
            post.user_profile = current_profile

            post.save()
            post_form = PostForm()
            return HttpResponseRedirect(reverse("index"))

    else:
        post_form = PostForm()

    

    return render(request, "index.html", context={"posts":posts,
                                                           "current_user":current_user,
                                                           "current_profile":current_profile,
                                                           "post_form":post_form,
                                                           "comments":comments})


def post(request, id):
    post = Post.objects.get(id = id)
    comments = Comment.objects.filter(post__id=id)
    current_user = request.user
    current_profile = UserProfile.objects.get(post=id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = current_user
            comment.post = post
            comment.save()
            comment_form = CommentForm()
            return redirect("post", post.id)

    else:
        comment_form = CommentForm()

    return render(request, "post.html", context={"post":post,
                                                          "current_user":current_user,
                                                          "current_profile":current_profile,
                                                          "comment_form":comment_form,
                                                          "comments":comments,})


def like(request, id):
    post = Post.objects.get(id = id)
    post.likes += 1
    post.save()
    return HttpResponseRedirect(reverse("index"))


def like_post(request, id):
    post = Post.objects.get(id = id)
    post.likes += 1
    post.save()
    return redirect("post", post.id)


@login_required(login_url='/accounts/login/')
def search(request):
    if 'profile' in request.GET and request.GET["profile"]:
        search_term = request.GET.get("profile")
        searched_user = UserProfile.search_by_user(search_term)
        message = f"{search_term}"
        user = User.objects.all()
        context = {
            "user":user,
            "message":message,
            "profile":searched_user
        }
        return render(request,'search_results.html',context)

    else:
        message = "You haven't searched for any term"
        return render(request, 'search_results.html',{"message":message})

 
    

@login_required(login_url='/accounts/login/')
def profile(request, id):
    user = User.objects.get(id=id)
    profile = UserProfile.objects.get(user_id=user)
    posts = Post.objects.filter(profile__id=id)
    return render(request, "profile.html", context={"user":user,"profile":profile,"posts":posts})

# def user_login(request):
    
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(username=username, password=password)

#         if user:

#             if user.is_active:
#                 login(request, user)

#                 return HttpResponseRedirect(reverse("index"))
#             else:
#                 return HttpResponseRedirect(reverse("user_login")) #raise error/ flash

#         else:
#             return HttpResponseRedirect(reverse("user_login")) #raise error/ flash
#     else:
#         return render(request, "registration/login.html", context={})




# def register(request):
#     registered = False
    

#     if request.method == "POST":
#         user_form = UserForm(request.POST)
        
#         if user_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()

#             user_profile = UserProfile()
#             user_profile.user = user
#             # user_profile.save()
#             user_profile.save()
#             registered = True
            

#             return HttpResponseRedirect(reverse("user_login"))

#         else:
#             pass

#     else:
#         user_form = UserForm()
        

#     return render(request, "registration/registration.html", context={"user_form":user_form,
#                                                           "registered":registered})

def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
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


@login_required(login_url='/accounts/login/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login"))