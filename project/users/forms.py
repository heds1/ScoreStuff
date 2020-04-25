from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from allauth.account.forms import LoginForm
from django.utils.translation import gettext, gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


# add to django-allauth LoginForm (change html)
# going off this: https://medium.com/@gavinwiener/modifying-django-allauth-forms-6eb19e77ef56
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        
        # add to all form fields
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'autofocus': '',
                'autocapitalize': 'none',
                'autocomplete': 'none',
                'maxlength': '30',
            })

        # add to specific form fields
        self.fields['login'].widget.attrs.update({
            'placeholder': 'Email',
            'aria-label': 'Email'
        })
