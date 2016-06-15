from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^doctor-list/', views.doctor_list, name='doctor_list'),
    url(r'^asm-list/', views.asm_list, name='asm_list'),
    url(r'^mr-list/', views.mr_list, name='mr_list'),
    #url(r'^hq-list/(\d{1,2})$', views.mr_hq_list, name='mr_hq_list'),
    url(r'^hq-list/$', views.hq_list, name='hq_list'),
    url(r'^state-list/', views.state_list, name='state_list'),
    url(r'^country-list/', views.country_list, name='country_list'),
    url(r'^grp-list/', views.grp_list, name='grp_list'),
    #url(r'^doctor-list/', views.doctor_list, name='doctor_list'),
    url(r'^chemist-list/', views.chemist_list, name='chemist_list'),
    url(r'^product-list/', views.product_list, name='product_list'),
    url(r'^emp-list/', views.emp_list, name='emp_list'),
    url(r'^doctor-list/([0-9]+)/$', views.doctor_list, name='doctor_list'),
    url(r'^user-list/', views.user_list, name='user_list'),
    #url(r'^doctor-list/', views.doctor_list, name='doctor_list'),
]
