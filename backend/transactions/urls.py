from django.urls import path
from . import views
urlpatterns=[path("",views.dashboard,name="dashboard"),path("transactions/new/",views.create,name="transaction_create"),path("transactions/<int:pk>/",views.detail,name="detail"),path("reports/transactions.csv",views.export_csv,name="export_csv")]
