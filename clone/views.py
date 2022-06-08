from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Post, User, UserProfile, Comment
from .forms import CommentForm, PostForm, RegisterForm
from django.contrib import messages

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            f_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=f_password)
            messages.success(request, 'Account was created for ' + user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/registration.html', {'form': form})

def login(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('/')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'registration/login.html', context)


@login_required
def index(request):
    current_user = request.user
    print(current_user)
    current_profile = UserProfile.objects.get(user_id=current_user)
    posts = Post.objects.all()[::-1]
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

    return render(request, "instagram/index.html", context={"posts":posts,
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

    return render(request, "instagram/post.html", context={"post":post,
                                                          "current_user":current_user,
                                                          "current_profile":current_profile,
                                                          "comment_form":comment_form,
                                                          "comments":comments,})