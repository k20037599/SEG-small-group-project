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
        return user_list(request, users)
    return redirect('/profile')


@login_required
def view_officers(request):
    current_user = request.user
    if current_user.user_type == "OWNER":
        users = User.objects.all().filter(user_type="OFFICER")
        return user_list(request, users)
    return redirect('/profile')


@login_required
def view_members(request):
    current_user = request.user
    if (current_user.user_type == "MEMBER" or current_user.user_type == "OFFICER" or current_user.user_type == "OWNER"):
        users = User.objects.all().filter(user_type="MEMBER")
        return user_list(request, users)
    return redirect('/profile')


@login_required
def user_list(request, users):
    return render(request, 'user_list.html', {'users': users})


@login_required
def show_user(request, user_id):
    current_user = request.user
    all_info = False
    try:
        user = User.objects.get(id=user_id)
        if (user.user_type == "APPLICANT" or user.user_type == "MEMBER") and current_user.user_type == "OFFICER":
            all_info = True
        if (user.user_type == "OFFICER" or user.user_type == "MEMBER") and current_user.user_type == "OWNER":
            all_info = True
    except User.DoesNotExist:
        return redirect('profile')
    return render(request, 'profile.html', {'profile_user': user, 'all_info': all_info})


@login_required
def profile(request):
    return render(request, 'profile.html', {'profile_user': request.user, 'all_info': False})


@login_required
def edit_profile(request):
    current_user = request.user
    if (request.method == 'POST'):
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS,
                                 "Profile Successfully updated!")
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
    return render(request, 'log_in.html', {'form': form, 'next': next})


def demote_officer(request, user_id):
    current_user = request.user
    try:
        user = User.objects.get(id=user_id)
        if (user.user_type == "OFFICER") and current_user.user_type == "OWNER":
            current_user.demote_officer(user)
            return show_user(request, user_id)
    except User.DoesNotExist:
        return redirect('profile')
    return redirect('profile')


def promote_member(request, user_id):
    current_user = request.user
    try:
        user = User.objects.get(id=user_id)
        if (user.user_type == "MEMBER") and current_user.user_type == "OWNER":
            current_user.promote_member(user)
            return show_user(request, user_id)
    except User.DoesNotExist:
        return redirect('profile')
    return redirect('profile')


def transfer_ownership(request, user_id):
    current_user = request.user
    try:
        user = User.objects.get(id=user_id)
        if (user.user_type == "OFFICER") and current_user.user_type == "OWNER":
            current_user.transfer_ownership(user)
            return show_user(request, user_id)
    except User.DoesNotExist:
        return redirect('profile')
    return redirect('profile')


@login_required
def log_out(request):
    logout(request)
    return redirect('home')
