from datetime import date
from django.core.exceptions import PermissionDenied,ValidationError
from django.test import TestCase
from accounts.models import Department,User
from .models import Entity,Transaction
from .services import add_workdays,close_transaction,transfer_transaction,visible_transactions
class WorkflowTests(TestCase):
 def setUp(self):
  self.a=Department.objects.create(name="الخدمات الرعوية",sla_days=3);self.b=Department.objects.create(name="الشؤون المالية",sla_days=2);self.entity=Entity.objects.create(name="جهة اختبار",entity_type="جمعية")
  self.reg=User.objects.create_user("reg",password="StrongPass!123",role="registrar",department=self.a,must_change_password=False);self.other=User.objects.create_user("other",password="StrongPass!123",role="registrar",department=self.b,must_change_password=False);self.router=User.objects.create_user("router",password="StrongPass!123",role="router",department=self.a,must_change_password=False)
 def make(self,kind="و",dept=None,user=None):return Transaction.objects.create(kind=kind,entity=self.entity,subject="معاملة اختبار",department=dept or self.a,created_by=user or self.reg)
 def test_independent_numbering(self):
  self.assertEqual(self.make("و").reference[-4:],"0001");self.assertEqual(self.make("ص").reference[-4:],"0001");self.assertEqual(self.make("و").reference[-4:],"0002")
 def test_department_scope_is_server_side(self):
  own=self.make();foreign=self.make(dept=self.b,user=self.other);self.assertIn(own,visible_transactions(self.reg));self.assertNotIn(foreign,visible_transactions(self.reg))
 def test_workdays_skip_friday_saturday(self):self.assertEqual(add_workdays(date(2026,9,10),1),date(2026,9,13))
 def test_transfer_requires_router_and_comment(self):
  item=self.make()
  with self.assertRaises(PermissionDenied):transfer_transaction(item=item,user=self.reg,to_department=self.b,comment="سبب")
  with self.assertRaises(ValidationError):transfer_transaction(item=item,user=self.router,to_department=self.b,comment="")
  transfer_transaction(item=item,user=self.router,to_department=self.b,comment="للمراجعة");item.refresh_from_db();self.assertEqual(item.department,self.b)
 def test_financial_close_requires_attachment(self):
  item=self.make(dept=self.b)
  with self.assertRaises(ValidationError):close_transaction(item=item,user=self.router)
 def test_force_password_change(self):
  user=User.objects.create_user("first",password="StrongPass!123",role="registrar",department=self.a,must_change_password=True);self.client.force_login(user);self.assertRedirects(self.client.get("/"),"/password/change/")
