from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout

from leaves.models import Admin,Staff, LeaveRecord

import uuid

# Create your views here.

def index(request):
    return render(request,'login.html')

def login(request):
    if request.POST['login_type']=="select":
        messages.error(request,'Choose the login type')
        return redirect('/')
    
    if request.POST['login_type'] == "admin":
        
        if(Admin.objects.filter(a_id=request.POST['faculty_id']).exists()):

            user = Admin.objects.filter(a_id=request.POST['faculty_id'])[0]

            if user.password == request.POST['password']:
                print("admin")
                request.session['id']=user.id
                return redirect(admin_dashboard)
            else:
                messages.error(request,"Wrong Password")
                return redirect('/')

        else:
            messages.error(request,"ID doesn't exist")
            return redirect('/')
        
    else:
        if(Staff.objects.filter(f_id=request.POST['faculty_id']).exists()):

            user = Staff.objects.filter(f_id=request.POST['faculty_id'])[0]

            if user.password == request.POST['password']:
                print("staff")
                request.session['id']=user.id
                return redirect(staff_dashboard)
            else:
                messages.error(request,"Wrong Password")
                return redirect('/')
        else:
            messages.error(request,"ID doesn't exist")
            return redirect('/')
        
        #return redirect(loginasstaff)

def change_staff_password(request):
    return render(request,'change_password.html')

def change_password(request):
    try:
        Staff.objects.filter(id=request.session['id']).update(password = request.POST['password'])
        messages.add_message(request,messages.INFO,"Password Updated")
    except:
        messages.add_message(request,messages.INFO,"Failed to Update")
        return redirect(staff_dashboard)
    return redirect(index)

def app_leave(request):
    return render(request,'app_leave.html')

def save_leave(request):
    uid = uuid.uuid1()
    uid = uid.fields[0]
    print(uid)
    
    staff = Staff.objects.filter(id=request.session['id'])[0]
    if staff.leaves_remaining > 0:
        if request.POST['no_of_days']>'3':
            print("donot save")
            messages.error(request,"Sorry! You have exceeded the limit")
            return redirect(app_leave)
        else:
            new_leave = LeaveRecord.objects.create(
                l_id = uid,
                f_id = staff.f_id,
                name = staff.name,
                dept = staff.dept,
                desc = request.POST['desc'],
                no_of_days = request.POST['no_of_days'],
                from_date = request.POST['start_date'],
                to_date = request.POST['end_date'],
                status = "Pending"
            )
            new_leave.save()
            messages.add_message(request,messages.INFO,"Application Sent")
    else:
        messages.error(request,"Sorry!! You consumed all the leaves")
        
    return redirect(staff_dashboard)

def past_app(request):
    staff = Staff.objects.filter(id=request.session['id'])[0]
    leaves = LeaveRecord.objects.filter(f_id = staff.f_id)
    context = {
        "leaves":leaves
        }
    
    return render(request,'past_app.html',context)
    #return HttpResponse("past_app")

def logout(request):
    #logout(request)
    messages.add_message(request,messages.INFO,"LOGGED OFF")
    return redirect('/')

def update_max_days(request):
    return render(request,'update_max_days.html')

def updated(request):
    print(1)
    ans = request.POST['yesorno']
    if ans == "Yes":
        Staff.objects.all().update(leaves_remaining=11)
        Staff.objects.all().update(leaves_used=0)
        messages.add_message(request,messages.INFO,"UPDATED SUCCESSFULLY")
    else:
        messages.add_message(request,messages.INFO,"NOT UPDATED")
    return render(request,'admin_dashboard.html')


def add_faculty(request):
    return render(request,'register.html')

def save_faculty(request):
    staff = Staff.objects.create(
        name = request.POST['name'],
        f_id = request.POST['f_id'],
        dept = request.POST['dept'],
        desig = request.POST['desig'],
        gender = request.POST['gender'],
        phone_no = request.POST['phone_no'],
        email = request.POST['email'],
        age = request.POST['age'],
        date_of_join = request.POST['doj'],
        leaves_used = request.POST['leaves_used'],
        leaves_remaining = request.POST['leaves_remaining'],
        password = request.POST['pass']
    )
    staff.save()
    messages.add_message(request,messages.INFO,"ADDED SUCCESSFULLY")
    return render(request,'admin_dashboard.html')


def staff_dashboard(request):
    user = Staff.objects.get(id=request.session['id'])
    print("staff_dashboard",type(user))
    context={
        "f_id" : user.f_id,
        "name" : user.name,
        "desig": user.desig,
        "dept" : user.dept,
        "email": user.email,
        "phone_no": user.phone_no,
        "total_leaves":user.total_leaves,
        "leaves_used":user.leaves_used,
        "leaves_remaining":user.leaves_remaining
    }
    return render(request,'dashboard.html',context)


def admin_dashboard(request):
    leaves = LeaveRecord.objects.filter(status = "Pending")
    print(leaves)
    context = {
        "staffs":leaves}
    return render(request,'admin_dashboard.html',context)

def admin_leave_record(request):
    leaves = LeaveRecord.objects.all()
    context = {
        "leaves":leaves
        }
    return render(request,'leave_record.html',context)



def view_staff(request,l_id):
    print(l_id)

    leave = LeaveRecord.objects.filter(l_id = l_id)[0]
    staff = Staff.objects.get(f_id = leave.f_id)
    context = {
        "l_id" : l_id,
        "f_id" : staff.f_id,
        "name" : staff.name,
        "desig": staff.desig,
        "dept" : staff.dept,
        "email": staff.email,
        "phone_no": staff.phone_no,
        "total_leaves":staff.total_leaves,
        "leaves_used":staff.leaves_used,
        "leaves_remaining":staff.leaves_remaining
    }
    return render(request,'view_staff.html',context)

def approve_leave(request,l_id):
    print("approve leave",l_id)
    leave = LeaveRecord.objects.get(l_id = l_id)
    staff = Staff.objects.get(f_id = leave.f_id)
    LeaveRecord.objects.filter(l_id = l_id).update(status = "Approved")
    Staff.objects.filter(f_id = leave.f_id).update(leaves_used = staff.leaves_used+leave.no_of_days)
    Staff.objects.filter(f_id = leave.f_id).update(leaves_remaining = staff.leaves_remaining-leave.no_of_days)
    print(staff.leaves_used,staff.leaves_remaining)
    
    return redirect(admin_dashboard)

def reject_leave(request,l_id):
    print("reject leave",l_id)
    #leave = LeaveRecord.objects.get(l_id = l_id)
    LeaveRecord.objects.filter(l_id = l_id).update(status = "Rejected")
    return redirect(admin_dashboard)

