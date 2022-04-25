from django.contrib import admin


from .models import Bill,BillDetail
# Register your models here.

class BillAdmin(admin.ModelAdmin):
    list_display = ["code","name","phone"]
    model = Bill

class BillDetailAdmin(admin.ModelAdmin):
    list_display = ["id","billCode"]
    model = BillDetail



admin.site.register(Bill, BillAdmin)
admin.site.register(BillDetail, BillDetailAdmin)