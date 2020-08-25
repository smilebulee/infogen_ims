from django.db import models

# Create your models here.

class Tb_tpt(models.Model):
    test_id = models.CharField(max_length=10, help_text="id", primary_key=True)
    text_data = models.CharField(max_length=30, null=True, blank=True, help_text="text")
    reg_user = models.CharField(max_length=30, null=True, blank=True, help_text="text")

class Tb_tpt2(models.Model):
    test_id = models.CharField(max_length=10, help_text="id", primary_key=True)
    text_data = models.CharField(max_length=30, null=True, blank=True, help_text="text")
    reg_user = models.CharField(max_length=30, null=True, blank=True, help_text="text")