from django.db import models
from datetime import datetime

# Create your models here.
class Cd_grp(models.Model):
    grp_cd = models.CharField(max_length=10, help_text="그룹",primary_key=True)
    grp_nm = models.TextField(help_text="그룹명")
    sort_ord = models.IntegerField(default=999, help_text="정렬순서")
    create_id = models.CharField(max_length=20, null=True, blank=True, help_text="등록자")
    create_dt = models.DateTimeField(default=datetime.now, help_text="등록일")
    update_id = models.CharField(max_length=20, null=True, blank=True, help_text="수정자")
    update_dt = models.DateTimeField(default=datetime.now, help_text="수정일")

class Cd(models.Model):
    grp_cd = models.ForeignKey('Cd_grp', on_delete=models.CASCADE)
    cmm_cd = models.CharField(max_length=10, help_text="코드")
    cmm_nm = models.TextField(help_text="코드명")
    sort_ord = models.IntegerField(default=999, help_text="정렬순서")
    create_id = models.CharField(max_length=20, null=True, blank=True, help_text="등록자")
    create_dt = models.DateTimeField(default=datetime.now, help_text="등록일")
    update_id = models.CharField(max_length=20, null=True, blank=True, help_text="수정자")
    update_dt = models.DateTimeField(default=datetime.now, help_text="수정일")
    class Meta:
        unique_together = (('grp_cd', 'cmm_cd'),)