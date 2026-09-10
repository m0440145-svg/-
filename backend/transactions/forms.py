from django import forms
from .models import Transaction
class TransactionForm(forms.ModelForm):
 class Meta:model=Transaction;fields=["kind","entity","date","subject","external_reference","external_date","channel","identity_number","confidentiality","priority","department","assignee","keywords","linked_transaction"]
 def clean_identity_number(self):
  v=self.cleaned_data.get("identity_number","")
  if v and (len(v)!=10 or not v.isdigit()):raise forms.ValidationError("رقم الهوية يجب أن يكون 10 أرقام")
  return v
