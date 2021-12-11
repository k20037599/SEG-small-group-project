'''Models for clubs applcation'''
from django.db import models
from libgravatar import Gravatar
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator

'''User model'''
class User(AbstractUser):
    class Meta:
        ordering = ['username']
        
    username = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        validators=[RegexValidator(
            regex=r'^\w{3,}$',
            message="Username must contain at least 3 letters or numbers"
        )]
    )

    first_name = models.CharField(
        max_length=50,
        blank=False,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z]{3,}$',
            message="First name must contain at least 3 letters"
        )]
    )

    last_name = models.CharField(
        max_length=50,
        blank=False,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z]{3,}$',
            message="Last name must contain at least 3 letters"
        )]
    )

    email = models.EmailField(
        max_length=50,
        unique=True,
        blank=False,
        validators=[EmailValidator(
            message="Email must begin with a username followed by an @ then by a domain name then by a . and domain e.g. .com"
        )]
    )

    experience_level_choices = (
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    )

    experience_level = models.CharField(
        max_length=20, choices=experience_level_choices, default='BEGINNER')

    personal_statement = models.CharField(max_length=500, blank=True)

    bio = models.CharField(max_length=300, blank=True)

    user_type = models.CharField(max_length=20, default='APPLICANT')

    application_status = models.CharField(max_length=20, default='PENDING')
    
    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)


    def demote_officer(self, user):
        user.user_type = 'MEMBER'
        user.save()

    def promote_member(self, user):
        user.user_type = 'OFFICER'
        user.save()

    def transfer_ownership(self, user):
        user.user_type = 'OWNER'
        user.save()
        self.user_type = 'OFFICER'
        self.save()
        
    def accept_application(self, user):
        user.user_type = 'MEMBER'
        user.application_status = 'ACCEPTED'
        user.save()

    def reject_application(self, user):
        user.application_status = 'REJECTED'
        user.save()

