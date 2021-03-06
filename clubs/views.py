from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from .forms import LogInForm, SignUpForm, UserForm, PasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.template import Template, Context
from .helpers import login_prohibited
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.core.paginator import Paginator
from django.conf import settings

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
        return user_list(request, users, "Applicants")
    return redirect('/profile')

"""
If the current user is an owner
then the owner can view a list of officers
"""
@login_required
def view_officers(request):
    current_user = request.user
    if current_user.user_type == "OWNER":
        users = User.objects.all().filter(user_type="OFFICER")
        return user_list(request, users, "Officers")
    return redirect('/profile')

"""
If the current user is an officer
Then the officer can view a list of members
"""
@login_required
def view_members(request):
    current_user = request.user
    if (current_user.user_type == "MEMBER" or current_user.user_type == "OFFICER" or current_user.user_type == "OWNER"):
        users = User.objects.all().filter(user_type="MEMBER")
        return user_list(request, users, "Members")
    return redirect('/profile')

"""
A view containing a list of all given users
"""
@login_required
def user_list(request, users, user_type):
    paginator = Paginator(users, settings.USERS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user_list.html', {'users':page_obj, 'user_type':user_type})

"""
Responsible for displaying a particular user based on user_id
"""
@login_required
def show_user(request, user_id):
    current_user = request.user
    all_info = False
    try:
        user = User.objects.get(id=user_id)
        #Decides whether the user will be able to see all information
        if (user.user_type == "APPLICANT" or user.user_type == "MEMBER") and current_user.user_type == "OFFICER":
            all_info = True
        if (user.user_type == "OFFICER" or user.user_type == "MEMBER") and current_user.user_type == "OWNER":
            all_info = True
    except User.DoesNotExist:
        return redirect('profile')
    return render(request, 'profile.html', {'profile_user': user, 'all_info': all_info})

"""
Renders all the information of the request user's profile
"""
@login_required
def profile(request):
    return render(request, 'profile.html', {'profile_user': request.user, 'all_info': False})


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
            messages.add_message(request, messages.SUCCESS,
                                 "Profile Successfully updated!")
            form.save()
            return redirect('/profile')
    else:
        form = UserForm(instance=current_user)
    return render(request, 'edit_profile.html', {'form': form})

"""
A view to edit the current users password
Contains a password form, and if the form data is valid then the form can be saved
and a success massage is displayed, the user is redirected to profile
"""
@login_required
def password(request):
    current_user = request.user
    if request.method == 'POST':
        form = PasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if check_password(password, current_user.password):
                new_password = form.cleaned_data.get('new_password')
                current_user.set_password(new_password)
                current_user.save()
                login(request, current_user)
                messages.add_message(request, messages.SUCCESS, "Password Updated Successfully")
                return redirect('/profile')
        else:
            messages.add_message(request, messages.ERROR, "Password Not Updated - Error")

    form = PasswordForm()
    return render(request, 'password.html', {'form':form})

"""
Allows a user to sign up by taking input from the sign up form.
If the form is valid then create the user and login.
If the form is invalid then display error message
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
    return render(request, 'log_in.html', {'form': form, 'next': next})

"""
Allow an owner to demote an officer, changing their user type back
to MEMBER.
If the user they are trying to demote doesn't exist, the owner will be redirected to
their profile.
"""
@login_required
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

"""
Allow an owner to promote a member, changing their user type to
to OFFICER.
If the user they are trying to promote doesn't exist, the owner will be redirected to
their profile.
"""
@login_required
def promote_member(request, user_id):
    current_user = request.user
    try:
        user = User.objects.get(id=user_id)
        if (user.user_type == "MEMBER") and (current_user.user_type == "OWNER"):
            current_user.promote_member(user)
            return show_user(request, user_id)
    except User.DoesNotExist:
        return redirect('profile')
    return redirect('profile')

"""
Allow the owner to make an officer the owner and demote themselved.
If the user they are trying to promote doesn't exist, the owner will be redirected to
their profile.
"""
@login_required
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

"""
Allow an officer to accept an application and change the user's
status to ACCEPTED.
If the conditions aren't met, redirect to the officer's profile.
"""
@login_required
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
Allow an officer to reject an application and change the user's
status to REJECTED.
If the conditions aren't met, redirect to the officer's profile.
"""
@login_required
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
