from cProfile import label
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import RegistrationUser
# from .signals import user_registered


# Registration user------------------------------------------------------------------
class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(max_length=150, label='* Username', help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    password1 = forms.CharField(widget=forms.PasswordInput(), help_text=password_validation.password_validators_help_text_html(), label='* Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='* Password confirmation', help_text='Enter the same password as before, for verification.')
    email = forms.EmailField(required=True, help_text='On your email will be send link to activate your porfile', label='* Email')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')


# Registration user extra information------------------------------------------------------------------
class MyRegisterUserForm(forms.ModelForm):
    birth = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='* Birthday')
    info = forms.CharField(widget=forms.Textarea(), required=False)
    class Meta:
        model = RegistrationUser
        fields = ('info', 'birth', 'gender')
        labels = {
            'gender': '* Gender',
        }
        widgets = {
            'info': CKEditorUploadingWidget()
        }


# Change user info------------------------------------------------------------------------------
class ChangeUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')




# Login user------------------------------------------------------------------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())


# Change password ------------------------------------------------------------------
class ChangePassForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(), label='Old password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(), label='New password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label='New password confirmation')