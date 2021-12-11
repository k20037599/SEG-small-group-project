"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clubs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_in/', views.log_in, name='log_in'),
    path('profile/', views.profile, name='profile'),
    path('show_user/<int:user_id>', views.show_user, name='show_user'),
    path('log_out/', views.log_out, name='log_out'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('view_applications/', views.view_applications, name='view_applications'),
    path('view_members/', views.view_members, name='view_members'),
    path('view_officers/', views.view_officers, name='view_officers'),
    path('demote_officer/<int:user_id>', views.demote_officer, name='demote_officer'),
    path('promote_member/<int:user_id>', views.promote_member, name='promote_member'),
    path('transfer_ownership/<int:user_id>', views.transfer_ownership, name='transfer_ownership'),
    path('password/', views.password, name='password'),
    path('accept_application/<int:user_id>',views.accept_application,name='accept_application'),
    path('reject_application/<int:user_id>',views.reject_application,name='reject_application'),
]
