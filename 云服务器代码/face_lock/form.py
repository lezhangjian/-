from django import forms



class RegisterForm(forms.Form):
    username = forms.CharField(min_length=6,max_length=30)
    password = forms.CharField(min_length=6, max_length=30)
    password_repeat = forms.CharField(min_length=6, max_length=30)