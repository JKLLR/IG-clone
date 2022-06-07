from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html') 

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
		return redirect('insta')
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