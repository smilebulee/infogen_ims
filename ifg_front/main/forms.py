from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password') #, 'email'

        widgets = {
            'username': forms.TextInput(attrs={'id':'username', 'class': 'form-control', 'placeholder': 'ID', 'value':''}),
            #'email': forms.EmailInput(attrs={'id':'email', 'class': 'form-control', 'value':'bulee@infogen.co.kr', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'id':'password', 'class': 'form-control', 'value':'', 'placeholder': 'Password'})
        }
        labels = {
            'username': '아이디',
            #'email': '이메일',
            'password': '패스워드'
        }
        # 글자수 제한

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['maxlength'] = 15
