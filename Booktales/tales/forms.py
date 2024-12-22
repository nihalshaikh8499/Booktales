from django import forms 
from .models import Tales
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TalesForm(forms.ModelForm):
    class Meta:
        model = Tales
        fields = ['title','text', 'photo']
        
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields =  ('username', 'email', 'password1', 'password2')