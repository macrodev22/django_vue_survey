from typing import Any
from django import forms

class RegisterForm(forms.Form):
    fullname = forms.CharField(max_length=120, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=8, required=True)
    password_confirm = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        # Password validation
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Password and password confirmation do not match")
        
        return cleaned_data
    
class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)