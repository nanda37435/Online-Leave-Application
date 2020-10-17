from django.contrib import admin

# Register your models here.

from leaves.models import Admin, Staff, LeaveRecord

admin.site.register(Admin)
admin.site.register(Staff)
admin.site.register(LeaveRecord)
