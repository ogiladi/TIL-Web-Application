from django import forms

class LoginForm(forms.Form):
    client_id = forms.CharField(label='Client id', max_length=256)
    client_secret = forms.CharField(label='Client secret', max_length=256)
    num_posts = forms.IntegerField(label='Number of posts')