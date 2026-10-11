from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="We'll use this email if we need to contact you."
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]