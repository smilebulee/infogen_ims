from django.db import models

# Create your models here.

# 공지사항 파일업로드 임시추가
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')