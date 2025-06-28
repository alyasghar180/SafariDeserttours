from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()

class EmailPhoneUsernameAuthenticationBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with either
    username, email, or phone number.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
            
        try:
            # Check if the provided username is actually an email, username, or phone number
            user = UserModel.objects.filter(
                Q(username__iexact=username) | 
                Q(email__iexact=username) | 
                Q(phone_number__iexact=username)
            ).first()
            
            if user and user.check_password(password):
                return user
                
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user
            UserModel().set_password(password)
            
        return None
