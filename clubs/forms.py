from django import forms
from .models import User
from django.core.validators import RegexValidator

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ['username', 'first_name', 'last_name', 'email', 'experience_level', 'personal_statement', 'bio',]

        widgets = {
            'personal_statement':forms.Textarea(),
            'bio':forms.Textarea(),
            'experience_level':forms.Select(choices=User.experience_level_choices)
            }

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        max_length=50,
        validators=[
        RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$' ,
            message="Password must contain at least one uppercase and number.")])

    password_confirm = forms.CharField(label="Password Confirm", widget=forms.PasswordInput(), max_length=50)

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password_confirm', 'Confirmation doesnt match.')

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            experience_level=self.cleaned_data.get('experience_level'),
            personal_statement=self.cleaned_data.get('personal_statement'),
            bio=self.cleaned_data.get('bio'),
            password=self.cleaned_data.get('password')
            )

        return user