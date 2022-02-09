from django import forms
from .models import Post
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    pic = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ('title', 'text', 'pic',)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    '''
    def clean_password(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('User not found')

        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Wrong password')
        return username, password
    '''

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('User not found', code='User not found')
        return username

    def clean_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Wrong password', code='Wrong password')
        return password


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    redirect_checkbox = forms.BooleanField(label='Login after registration', required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if str(cd['email']).find('@gcore.lu') == -1:
            raise forms.ValidationError('Email must be in domen @gcore.lu')
        return cd['email']
