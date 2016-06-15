from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ppp/', views.ppp, name='ppp'),
    url(r'^ppp-list/', views.ppplist, name='ppp-list'),
    url(r'^ppp_new/$', views.ppp_new, name='ppp_new'),
    url(r'^ppp_new_2/(?P<ppp>.*)/$', views.ppp_new_2, name='ppp_new_2'),
    #url(r'^ppp_new_3/$', views.ppp_new_3, name='ppp_new_3'),
    url(r'^ppp_new_process/',views.ppp_new_process, name='ppp_new_process'),
    url(r'^ppp_new_process_2/(?P<ppp>.*)/$',views.ppp_new_process_2, name='ppp_new_process_2'),
    #url(r'^ppp_new_process_3/',views.ppp_new_process_3, name='ppp_new_process_3'),
    url(r'^pppRecord/', views.pppRecord, name='pppRecord'),
    url(r'^pppRecord-list/', views.pppRecord_list, name='pppRecord_list'),
    url(r'^ppp_new_record/',views.ppp_new_record, name='ppp_new_record'),
    url(r'^ppp-line/', views.ppp_line, name='ppp_line'),
    url(r'^pppline/(?P<ppp>.*)/$', views.pppline, name='pppline'),
    url(r'^ppp-data/', views.ppp_data, name='ppp_data'),
    url(r'^ppp-report/', views.ppp_report_data, name='ppp_report_data'),
    url(r'^pppApprove/', views.pppApprove, name='pppApprove'),
    url(r'^ppp-list-approve/', views.ppp_list_approve, name='ppp_list_approve'),
    url(r'^ppp-approve/(?P<appId>.*)/$', views.ppp_approve, name='ppp_approve'),
    url(r'^ppp_record_amount/',views.ppp_record_amount, name='ppp_record_amount'),
] 
