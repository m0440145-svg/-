from datetime import timedelta
from django.core.exceptions import PermissionDenied,ValidationError
from django.db import transaction as db_transaction
from django.utils import timezone
from .models import Event,Transaction
from transfers.models import Transfer
def visible_transactions(user):
 qs=Transaction.objects.select_related("department","entity","assignee")
 if user.role=="admin":return qs.none()
 if user.can_view_all:return qs
 return qs.filter(department=user.department)
def add_workdays(start,days,holidays=()):
 day=start;remaining=days
 while remaining:
  day+=timedelta(days=1)
  if day.weekday() not in (4,5) and day not in holidays:remaining-=1
 return day
@db_transaction.atomic
def transfer_transaction(*,item,user,to_department,comment):
 if user.role!="router":raise PermissionDenied
 if not comment.strip():raise ValidationError("تعليق التحويل إلزامي")
 if not visible_transactions(user).filter(pk=item.pk).exists():raise PermissionDenied
 old=item.department;item.department=to_department;item.status=Transaction.Status.PROCESSING;item.due_at=add_workdays(timezone.localdate(),to_department.sla_days);item.save(update_fields=["department","status","due_at","updated_at"]);Transfer.objects.create(transaction=item,from_department=old,to_department=to_department,comment=comment,transferred_by=user);Event.objects.create(transaction=item,action="تحويل",details=comment,actor=user,from_department=old,to_department=to_department);return item
def close_transaction(*,item,user):
 if user.role!="router":raise PermissionDenied
 if item.department.name=="الشؤون المالية" and not item.attachments.exists():raise ValidationError("لا يمكن إغلاق معاملة مالية دون مرفق")
 item.status=Transaction.Status.CLOSED;item.completed_at=timezone.now();item.save(update_fields=["status","completed_at","updated_at"]);Event.objects.create(transaction=item,action="إغلاق",actor=user)
