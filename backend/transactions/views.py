import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,redirect,render
from .forms import TransactionForm
from .models import Event,Transaction
from .services import add_workdays,visible_transactions
@login_required
def dashboard(request):
 qs=visible_transactions(request.user);return render(request,"transactions/dashboard.html",{"transactions":qs.order_by("-created_at")[:50],"late":qs.filter(status=Transaction.Status.LATE).count(),"total":qs.count()})
@login_required
def create(request):
 if request.user.role in {"viewer","admin"}:return HttpResponse("غير مصرح",status=403)
 form=TransactionForm(request.POST or None)
 if request.method=="POST" and form.is_valid():
  item=form.save(commit=False);item.created_by=request.user;item.due_at=add_workdays(item.date,item.department.sla_days);item.save();Event.objects.create(transaction=item,action="إنشاء",details="تسجيل المعاملة",actor=request.user,to_department=item.department);return redirect("detail",pk=item.pk)
 return render(request,"transactions/form.html",{"form":form})
@login_required
def detail(request,pk):
 item=get_object_or_404(visible_transactions(request.user),pk=pk);Event.objects.create(transaction=item,action="فتح",details="عرض التفاصيل",actor=request.user);return render(request,"transactions/detail.html",{"item":item})
@login_required
def export_csv(request):
 qs=visible_transactions(request.user);response=HttpResponse(content_type="text/csv; charset=utf-8");response.write("\ufeff");response["Content-Disposition"]='attachment; filename="transactions.csv"';w=csv.writer(response);w.writerow(["الرقم","النوع","الجهة","الموضوع","القسم","الحالة"])
 for x in qs:w.writerow([x.reference,x.get_kind_display(),x.entity.name,x.subject,x.department.name,x.get_status_display()])
 return response
