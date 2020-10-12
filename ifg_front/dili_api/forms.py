from django import forms
from django.contrib.auth.models import User

# 공지사항 파일업로드 임시추가
class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
