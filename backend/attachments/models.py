from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
class Attachment(models.Model):
 transaction=models.ForeignKey("transactions.Transaction",on_delete=models.CASCADE,related_name="attachments");file=models.FileField(upload_to="transactions/%Y/%m/",validators=[FileExtensionValidator(["pdf","png","jpg","jpeg"])]);original_name=models.CharField(max_length=255);size=models.PositiveIntegerField();uploaded_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT);created_at=models.DateTimeField(auto_now_add=True)
 def delete(self,*a,**k):raise PermissionError("لا يسمح بالحذف النهائي")
