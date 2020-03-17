from django.db import models

# Create your models here.
class Cmm_cd(models.Model):
    grp_cd = models.CharField(max_length=10, help_text="그룹")
    grp_nm = models.TextField(null=True, blank=True, help_text="그룹명")
    cmm_cd = models.CharField(max_length=10, help_text="코드")
    cmm_nm = models.TextField(help_text="코드명")
    sort_ord = models.IntegerField(help_text="정렬순서")
    create_id = models.CharField(max_length=20, null=True, blank=True, help_text="등록자")
    create_dt = models.DateTimeField(help_text="등록일")
    update_id = models.CharField(max_length=20, null=True, blank=True, help_text="수정자")
    update_dt = models.DateTimeField(help_text="수정일")
    class Meta:
        unique_together = (('grp_cd', 'cmm_cd'),)

class Emp(models.Model):
    emp_id = models.CharField(max_length=20, primary_key=True, help_text="사용자ID")
    emp_nm = models.CharField(max_length=20, help_text="사용자명")
    email = models.EmailField(help_text="E-mail")
    contact = models.CharField(max_length=15, null=True, blank=True, help_text="연락처")
    addr = models.TextField(null=True, blank=True, help_text="주소")
    birth = models.CharField(max_length=10, null=True, blank=True, help_text="생년월일")
