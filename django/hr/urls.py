from django.conf.urls import url

from . import views
urlpatterns = [
    #url(r'^', views.index, name='index'),
    url(r'^employee/', views.emp, name='emp'),
    url(r'^emp-list/', views.emp_list, name='emp_list'),
    url(r'^invite/', views.invite, name='invite'),
    url(r'^send_invite/', views.send_invite, name='send_invite'),
    url(r'^join/', views.join, name='join'),
    #url(r'^hq-list/(\d{1,2})$', views.mr_hq_list, name='mr_hq_list'),
    url(r'^employee_new/$', views.employee_new, name='employee_new'),
    url(r'^hr-policy/', views.hr_policy, name='hr_policy'),
    
    url(r'^employee_create/$', views.employee_create, name='employee_create'),
    url(r'^employee_create_process/$', views.employee_create_process, name='employee_create_process'),
    
    url(r'^employee_address/$', views.employee_address, name='employee_address'),
    url(r'^employee_address_process/$', views.employee_address_process, name='employee_address_process'),

    url(r'^employee_education/$', views.employee_education, name='employee_education'),  
    url(r'^emp_edu_details_read/$', views.emp_edu_details_read, name='emp_edu_details_read'),
    url(r'^emp_edu_details_write/(?P<a>.*)/$', views.emp_write, name='employee_edu_write'),
    url(r'^employee_education_process/$', views.employee_education_process, name='employee_education_process'),
    
    url(r'^employee_previous_details/$', views.employee_previous_details, name='employee_previous_details'),
    url(r'^emp_prev_employer_read/$', views.emp_prev_employer_read, name='emp_prev_employer_read'),
    url(r'^emp_prev_details_write/(?P<a>.*)/$', views.emp_prev_details_write, name='emp_prev_details_write'),
    url(r'^employee_previous_details_process/$', views.employee_previous_details_process, name='employee_previous_details_process'),
    
    url(r'^employee_family_details/$', views.employee_family_details, name='employee_family_details'),
    url(r'^emp_family_details_read/$', views.emp_family_details_read, name='emp_family_details_read'),
    url(r'^emp_family_details_write/(?P<a>.*)/$', views.emp_family_details_write, name='emp_family_details_write'),
    url(r'^employee_family_details_process/$', views.employee_family_details_process, name='employee_family_details_process'),
    
    url(r'^employee_medical_details/$', views.employee_medical_details, name='employee_medical_details'),
    url(r'^employee_medical_details_process/$', views.employee_medical_details_process, name='employee_medical_details_process'),

]
