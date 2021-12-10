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
from django.core.paginator import Paginator
from django.conf import settings

@login_prohibited
def home(request):
    return render(request, 'home.html')

@login_required
def view_applications(request):
    current_user = request.user
    if current_user.user_type == "OFFICER":
        users = User.objects.all().filter(user_type="APPLICANT")
        return user_list(request, users, "Applicants")
    return redirect('/profile')

@login_required
def view_members(request):
    current_user = request.user
    if current_user.user_type == "OFFICER":
        users = User.objects.all().filter(user_type="MEMBER")
        return user_list(request, users, "Members")
    return redirect('/profile')

@login_required
def user_list(request, users, user_type):
    paginator = Paginator(users, settings.USERS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user_list.html', {'users':page_obj, 'user_type':user_type})

@login_required
def show_user(request, user_id):
    current_user = request.user
    all_info = False
    try:
        user = User.objects.get(id=user_id)
        if (user.user_type == "APPLICANT" or user.user_type == "MEMBER") and current_user.user_type == "OFFICER":
            all_info = True
    except User.DoesNotExist:
        return redirect('profile')
    return render(request, 'profile.html', {'profile_user': user, 'all_info': all_info, 'application_status':current_user.application_status})

@login_required
def profile(request):
    application_status = request.user.application_status
    return render(request, 'profile.html', {'profile_user': request.user, 'all_info': False, 'application_status': application_status})

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

def accept_application(request, user_id):
    current_user = request.user
    try:
        applicant = User.objects.get(id=user_id)
        if (applicant.user_type == "APPLICANT" ) and current_user.user_type == "OFFICER":
            current_user.accept_application(applicant)
            return show_user(request, user_id)
    except User.DoesNotExist:
        return redirect('profile')
    return redirect('profile')


def reject_application(request, user_id):
    current_user = request.user
    try:
        applicant = User.objects.get(id=user_id)
        if (applicant.user_type == "APPLICANT" ) and current_user.user_type == "OFFICER":
            current_user.reject_application(applicant)
            return show_user(request, user_id)
    except User.DoesNotExist:
        return redirect('profile')
    return redirect('profile')

@login_required
def log_out(request):
    logout(request)
    return redirect('home')
