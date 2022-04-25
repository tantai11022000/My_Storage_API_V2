from django.urls import path
from . import views
urlpatterns = [
    path('bill-detail/<str:code>',views.get_bill_by_code,name="bill-detail"),
    path('create-bill',views.create_bill,name="create-bill"),
]