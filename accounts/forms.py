
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm

from accounts.models import Profile

UserModel = get_user_model()
class AppUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email",)
        field_classes = {"email": UsernameField}
        widgets = {"email": forms.EmailInput(attrs={"autofocus": True})}



class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel
        field_classes = {"email": UsernameField}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]

        labels = {
            'date_of_birth': "Date of Birth:",
            'profile_picture': "Profile Picture:",
        }