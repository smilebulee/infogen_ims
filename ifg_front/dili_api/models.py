from django.db import models
from datetime import datetime

# Create your models here.
class auth_user(models.Model):
    id = models.IntegerField(help_text="아이디",primary_key=True)
    password = models.CharField(max_length=128, null=True, help_text="비밀번호")
    last_login = models.DateTimeField(default=datetime.now, help_text="최종로그인일자")
    is_superuser = models.CharField(max_length=1, null=True, help_text="슈퍼유저여부")
    username = models.TextField(help_text="사용자명")
    first_name = models.TextField(help_text="이름")
    last_name = models.TextField(help_text="성")
    email = models.TextField(help_text="이메일")
    is_staff = models.CharField(max_length=1, null=True, help_text="관리자여부")
    is_active = models.CharField(max_length=1, null=True, help_text="활성화여부")
    date_joined = models.DateTimeField(default=datetime.now, help_text="수정일")

# 공지사항 파일업로드 임시추가
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')