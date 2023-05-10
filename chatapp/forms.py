from django import forms
from django.contrib.auth.models import User
class user_info_forms(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(),max_length=50, required=True)

    class Meta:
        model=User
        fields = ('username', 'password')