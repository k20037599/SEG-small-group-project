from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from .forms import LogInForm, SignUpForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.template import Template, Context
from .helpers import login_prohibited
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured

@login_prohibited
def home(request):
    return render(request, 'home.html')

@login_required
def view_applications(request):
    current_user = request.user
    if current_user.user_type == "OFFICER":
        users = User.objects.all().filter(user_type="APPLICANT")
        return user_list(request, users, True)
    return redirect('/profile')

@login_required
def user_list(request, users, all_info):
    return render(request, 'user_list.html', {'users': users, 'all_info': all_info})

@login_required
def show_user(request, user_id):
    try:
        context = User.objects.get(id=user_id)
        posts = Post.objects.filter(author=context)
    except User.DoesNotExist:
        return redirect('users')

    return render(request, 'show_user.html', {'user': context, 'posts':posts, 'following':following, 'followable':followable})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    current_user = request.user
    if (request.method == 'POST'):
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile Successfully updated!")
            form.save()
            return redirect('/profile')
    else:
        form = UserForm(instance=current_user)
    return render(request, 'edit_profile.html', {'form': form})

@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/profile')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        next = request.POST.get('next')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                redirect_url = next or 'profile'
                login(request, user)
                return redirect(redirect_url)
        messages.add_message(request, messages.ERROR,
                             "The credentials provided were invalid!")
    form = LogInForm()
    if request.method == 'GET':
         next = request.GET.get('next') or ''
    return render(request, 'log_in.html', {'form': form, 'next':next})

@login_required
def log_out(request):
    logout(request)
    return redirect('home')
