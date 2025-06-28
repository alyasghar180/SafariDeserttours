from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import UserProfile

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    Form for user registration with additional fields.
    """
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text=_('Required. Enter a valid email address.')
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        help_text=_('Optional. Enter your phone number.')
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('This email address is already in use.'))
        return email


class CustomAuthenticationForm(AuthenticationForm):
    """
    Form for user login that allows authentication with username, email, or phone number.
    """
    username = forms.CharField(
        label=_('Username, Email or Phone'),
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    
    error_messages = {
        'invalid_login': _(
            "Please enter a correct username/email/phone and password. "
            "Note that both fields may be case-sensitive."
        ),
        'inactive': _('This account is inactive.'),
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Username, Email or Phone')


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'date_of_birth', 'nationality', 'preferred_language', 
                 'emergency_contact_name', 'emergency_contact_number')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic user information.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(_('This email address is already in use.'))
        return email
