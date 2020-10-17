from django.db import models

# Create your models here.

class Admin(models.Model):
    a_id = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=225)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Staff(models.Model):
    name = models.CharField(max_length=225)
    f_id = models.CharField(max_length=225)
    desig = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    email = models.CharField(max_length=225)
    phone_no = models.CharField(max_length=225)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    date_of_join = models.DateField()
    total_leaves = models.IntegerField(default=11)
    leaves_used = models.IntegerField(default=0)
    leaves_remaining = models.IntegerField(default=11)
    password = models.CharField(max_length=100,default=None)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class LeaveRecord(models.Model):
    l_id = models.CharField(max_length=100,default=None)
    f_id = models.CharField(max_length=255)
    name = models.CharField(max_length=225)
    dept = models.CharField(max_length=100)
    no_of_days = models.IntegerField(default=1)
    desc = models.TextField(max_length=225)
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(max_length=20,default="Pending")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
