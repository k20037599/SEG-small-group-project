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

"""
The home view that renders the home page
"""
@login_prohibited
def home(request):
    return render(request, 'home.html')

"""
If the current user is an officer
then the officer can view a list of submitted applications
"""
@login_required
def view_applications(request):
    current_user = request.user
    if current_user.user_type == "OFFICER":
        users = User.objects.all().filter(user_type="APPLICANT")
        return user_list(request, users)
    return redirect('/profile')

"""
If the current user is an officer
Then the officer can view a list of members
"""
@login_required
def view_members(request):
    current_user = request.user
    if current_user.user_type == "OFFICER":
        users = User.objects.all().filter(user_type="MEMBER")
        return user_list(request, users)
    return redirect('/profile')

"""
A view containing a list of all users of the system
"""
@login_required
def user_list(request, users):
    return render(request, 'user_list.html', {'users': users})

"""
Responsible for displaying a particular user based on user_id
"""
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

"""
Renders all the information of the request user's profile
"""
@login_required
def profile(request):
    application_status = request.user.application_status
    return render(request, 'profile.html', {'profile_user': request.user, 'all_info': False, 'application_status': application_status})

"""
A view to edit the current users profile
Contains a user form, and if the form data is valid then the form can be saved
and a success massage is displayed, the user is redirected to profile
"""
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

"""
Creates a sign up form and if the entered info is valid
then save the form and redirect to the users profile
"""
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

"""
Logs the user in by taking input from the log in form
If the form is valid then authenticate the user and redirect them
to their profile.
If the form is invalid then display error message
"""
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

"""
Finds the applicant based on user_id
If the current User is an officer then call accept_application
function and pass in the applicant. Then display the accepted user
If the user does not exist then redirect to the users profile
"""
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

"""
Finds the applicant based on user_id
If the current User is an officer then call reject_application
function and pass in the applicant. Then display the rejected user
If the user does not exist then redirect to the users profile
"""
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

"""
Logs out and redirects to home page
"""
@login_required
def log_out(request):
    logout(request)
    return redirect('home')
