from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())


class CreateNewUserForm(forms.Form):
    name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())


class NewTweetForm(forms.Form):
    new_tweet = forms.CharField(widget=forms.Textarea, max_length=140)
