from django import forms
from django.utils.translation import gettext_lazy as _

from .models import PackageReview


class PackageReviewForm(forms.ModelForm):
    """
    Form for users to submit package reviews.
    """
    # Add name and email fields for anonymous users
    name = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your Name')})
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Your Email')})
    )
    
    class Meta:
        model = PackageReview
        fields = ['rating', 'title', 'comment', 'name', 'email']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Review Title')}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Your experience with this package')}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-select'})
        self.fields['rating'].empty_label = None
