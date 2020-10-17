from django.urls import path,include
from django.conf.urls import url
from django.conf import settings

from django.conf.urls.static import static
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^change_staff_password$',views.change_staff_password),
    url(r'^change_password$',views.change_password),
    url(r'^app_leave$',views.app_leave),
    url(r'^save_leave$',views.save_leave),
    url(r'^past_app$',views.past_app),
    url(r'^update_max_days$',views.update_max_days),
    url(r'^add_faculty$',views.add_faculty),
    url(r'^staff_dashboard$',views.staff_dashboard),
    url(r'^updated$',views.updated),
    url(r'^admin_dashboard$',views.admin_dashboard),
    url(r'^admin_leave_record$',views.admin_leave_record),
    url(r'^add_faculty$',views.add_faculty),
    url(r'^save_faculty$',views.save_faculty),
    url(r'^view_staff/(\d+)/',views.view_staff,name='l_id'),
    url(r'^approve_leave/(\d+)/',views.approve_leave,name='l_id'),
    url(r'^reject_leave/(\d+)/',views.reject_leave,name='l_id')
    ]

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
