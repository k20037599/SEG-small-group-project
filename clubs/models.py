from django.db import models
from libgravatar import Gravatar
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator

class User(AbstractUser):
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

    experience_level = (
        (0, 'Beginner'),
        (1, 'Intermmediate'),
        (2, 'Advanced'),
    )

    personal_statement = models.CharField(max_length=500, blank=True)

    bio = models.CharField(max_length=300, blank=True)

    user_type = ('Applicant')

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)
