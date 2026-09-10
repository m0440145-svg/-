from django.conf import settings
from django.db import models
class Transfer(models.Model):
 transaction=models.ForeignKey("transactions.Transaction",on_delete=models.CASCADE,related_name="transfers");from_department=models.ForeignKey("accounts.Department",on_delete=models.PROTECT,related_name="+");to_department=models.ForeignKey("accounts.Department",on_delete=models.PROTECT,related_name="+");comment=models.TextField();transferred_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT);created_at=models.DateTimeField(auto_now_add=True)
