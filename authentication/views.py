from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login, authenticate,logout
from django.conf import settings
from . import forms



def logout_user(request):
    logout(request)
    return redirect('login')

def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                message = 'Identifiants invalides.'
    return render(request, 'login.html', context={'form': form, 'message': message})


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request,user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    
    return render(request,'signup.html',context={'form':form})