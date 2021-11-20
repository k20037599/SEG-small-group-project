from django.db import models
from libgravatar import Gravatar
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
#from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

#This is for making the email the username, but wasn't working properly

# class UserManager(BaseUserManager):
#     def create_user(self, first_name, last_name, email, experience_level, personal_statement, bio, password, is_active):
#         email = self.normalize_email(email)
#         user = self.model(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             experience_level=experience_level,
#             personal_statement=personal_statement,
#             bio=bio,
#             is_active=is_active
#             )
#
#         user.set_password(password)
#         user.save(using=self._db)
#
#         return user
#
#     def create_superuser(self, first_name, last_name, email, experience_level, personal_statement, bio, password, is_active):
#         """ Create a new superuser profile """
#         user = self.model(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             experience_level=experience_level,
#             personal_statement=personal_statement,
#             bio=bio,
#             is_active=is_active
#             )
#         user.is_superuser = True
#
#         user.save(using=self._db)
#
#         return user

class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        validators=[RegexValidator(
            regex=r'^\w{3,}$' ,
            message="Username must contain at least 3 letters or numbers"
        )]
    )

    first_name = models.CharField(
        max_length=50,
        blank=False,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z]{3,}$' ,
            message="First name must contain at least 3 letters"
        )]
    )

    last_name = models.CharField(
        max_length=50,
        blank=False,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z]{3,}$' ,
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
    ##had to change this to strings as it wasnt working with numbers
    experience_level_choices = (
        ('BEGINNER', 'Beginner'),
        ('INTERMMEDIATE', 'Intermmediate'),
        ('ADVANCED', 'Advanced'),
    )

    experience_level = models.CharField(max_length=20, choices=experience_level_choices, default='BEGINNER')

    personal_statement = models.CharField(max_length=500, blank=True)

    bio = models.CharField(max_length=300, blank=True)

    user_type = ('Applicant')

    ##needed if we make the username=email
    #objects = UserManager()
    #USERNAME_FIELD = 'email'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)
