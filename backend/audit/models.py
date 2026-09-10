from django.conf import settings
from django.db import models
class AuditLog(models.Model):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.PROTECT);action=models.CharField(max_length=50);resource=models.CharField(max_length=80);resource_id=models.CharField(max_length=80,blank=True);details=models.JSONField(default=dict);ip=models.GenericIPAddressField(null=True);created_at=models.DateTimeField(auto_now_add=True)
 class Meta:ordering=["-created_at"];default_permissions=("view",)
 def save(self,*a,**k):
  if self.pk:raise PermissionError("سجل التدقيق غير قابل للتعديل")
  super().save(*a,**k)
 def delete(self,*a,**k):raise PermissionError("سجل التدقيق غير قابل للحذف")
