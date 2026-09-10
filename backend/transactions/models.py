from django.conf import settings
from django.db import models,transaction
from django.utils import timezone
from accounts.models import Department
class Entity(models.Model):
 name=models.CharField(max_length=200,unique=True);entity_type=models.CharField(max_length=100);contact_name=models.CharField(max_length=150,blank=True);phone=models.CharField(max_length=30,blank=True);email=models.EmailField(blank=True);active=models.BooleanField(default=True)
 def __str__(self):return self.name
class Counter(models.Model):
 year=models.PositiveSmallIntegerField();kind=models.CharField(max_length=1);value=models.PositiveIntegerField(default=0)
 class Meta:constraints=[models.UniqueConstraint(fields=["year","kind"],name="unique_counter_year_kind")]
class Transaction(models.Model):
 class Kind(models.TextChoices):OUT="ص","صادر";IN="و","وارد";INTERNAL="د","داخلي"
 class Confidentiality(models.TextChoices):NORMAL="normal","عادي";SECRET="secret","سري";TOP_SECRET="top_secret","سري جدًا"
 class Status(models.TextChoices):ROUTING="routing","قيد التحويل";PROCESSING="processing","قيد التنفيذ";DONE="done","منجزة";LATE="late","متأخرة";CLOSED="closed","مغلقة";CANCELLED="cancelled","ملغاة"
 reference=models.CharField(max_length=30,unique=True,editable=False);kind=models.CharField(max_length=1,choices=Kind.choices);entity=models.ForeignKey(Entity,on_delete=models.PROTECT);date=models.DateField(default=timezone.localdate);subject=models.CharField(max_length=400);external_reference=models.CharField(max_length=100,blank=True);external_date=models.DateField(null=True,blank=True);channel=models.CharField(max_length=30,blank=True);identity_number=models.CharField(max_length=10,blank=True);confidentiality=models.CharField(max_length=20,choices=Confidentiality.choices,default=Confidentiality.NORMAL);priority=models.CharField(max_length=20,default="عادية");department=models.ForeignKey(Department,on_delete=models.PROTECT,related_name="transactions");assignee=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.PROTECT,related_name="assigned_transactions");status=models.CharField(max_length=20,choices=Status.choices,default=Status.ROUTING);keywords=models.CharField(max_length=400,blank=True);linked_transaction=models.ForeignKey("self",null=True,blank=True,on_delete=models.PROTECT);due_at=models.DateField(null=True,blank=True);completed_at=models.DateTimeField(null=True,blank=True);cancelled_at=models.DateTimeField(null=True,blank=True);created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="created_transactions");created_at=models.DateTimeField(auto_now_add=True);updated_at=models.DateTimeField(auto_now=True)
 def save(self,*a,**k):
  if not self.reference:
   with transaction.atomic():
    year=timezone.localdate().year;c,_=Counter.objects.select_for_update().get_or_create(year=year,kind=self.kind);c.value+=1;c.save(update_fields=["value"]);self.reference=f"{self.kind}-{year}-{c.value:04d}"
  super().save(*a,**k)
class Event(models.Model):
 transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE,related_name="events");action=models.CharField(max_length=40);details=models.TextField(blank=True);actor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT);from_department=models.ForeignKey(Department,null=True,blank=True,on_delete=models.PROTECT,related_name="+");to_department=models.ForeignKey(Department,null=True,blank=True,on_delete=models.PROTECT,related_name="+");created_at=models.DateTimeField(auto_now_add=True)
 class Meta:ordering=["created_at"]
