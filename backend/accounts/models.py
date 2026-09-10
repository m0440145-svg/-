from django.contrib.auth.models import AbstractUser
from django.db import models
class Department(models.Model):
 name=models.CharField(max_length=150,unique=True);parent=models.ForeignKey("self",null=True,blank=True,on_delete=models.PROTECT,related_name="children");sla_days=models.PositiveSmallIntegerField(default=5);active=models.BooleanField(default=True)
 def __str__(self):return self.name
class User(AbstractUser):
 class Role(models.TextChoices):REGISTRAR="registrar","مسجّل";VIEWER="viewer","مطالعة فقط";ROUTER="router","محوّل";ADMIN="admin","مدير نظام"
 role=models.CharField(max_length=20,choices=Role.choices,default=Role.REGISTRAR);department=models.ForeignKey(Department,null=True,blank=True,on_delete=models.PROTECT);job_title=models.CharField(max_length=120,blank=True);must_change_password=models.BooleanField(default=True)
 @property
 def can_view_all(self):return self.role in {self.Role.VIEWER,self.Role.ROUTER}
 @property
 def can_manage_system(self):return self.role==self.Role.ADMIN
