
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm

from accounts.models import Profile

UserModel = get_user_model()
class AppUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email", 'first_name', 'last_name')
        field_classes = {"email": UsernameField}
        widgets = {"email": forms.EmailInput(attrs={"autofocus": True})}



class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel
        field_classes = {"email": UsernameField}


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        if self.user:
            self.fields['first_name'].initial = self.user.first_name  # fill the form with the relevant data from db
            self.fields['last_name'].initial = self.user.last_name

    class Meta:
        model = Profile
        exclude = ['user']

        labels = {
            'first_name': "First Name:",
            'last_name': "Last Name:",
            'date_of_birth': "Date of Birth:",
            'avatar': "Your Avatar:",
        }

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'avatar': forms.URLInput(attrs={'placeholder': 'ex: https://'})
        }

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']

            if commit:
                self.user.save()

        if commit:
            profile.save()

        return profile
