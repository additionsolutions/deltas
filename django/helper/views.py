from django.shortcuts import render

# Create your views here.
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.conf import settings
#from django.utils import simplejson
try: import simplejson as json
except ImportError: import json
from marketing.models import PPP
from marketing.models import Product
import xmlrpclib

# Returns first MR (User ID from Users Table) assigned to supplied HQ
def get_user_from_HQ(hq_id):
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))

    user_id = models.execute_kw(db, sys_uid, sys_password, 'res.users', 'search_read', [[['region_id','=',hq_id]]], {'fields': ['id']} )
    user_li = user_id[0]
    return  user_li['id']

# Returns Employee ID from HR.Employee table for the supplied User ID
def get_employee_from_user(user_id):
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    resource_id = models.execute_kw(db, sys_uid, sys_password, 'resource.resource', 'search_read', [[['active','=',True],['user_id','=',user_id]]], {'fields': ['id']})
    resource_id_li = resource_id[0]
    employee = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['resource_id','=', resource_id_li['id']],]], {'fields': ['id']} )
    employee_li = employee[0]
    return  employee_li['id']

# Returns Employee Name from HR.Employee table for the supplied User ID
def get_employee_name_from_user(user_id):
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    resource_id = models.execute_kw(db, sys_uid, sys_password, 'resource.resource', 'search_read', [[['active','=',True],['user_id','=',user_id]]], {'fields': ['id']})
    if resource_id:
    	resource_id_li = resource_id[0]
    else:
	return "Error: No Employee data for this user"
    employee = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['resource_id','=', resource_id_li['id']],]], {'fields': ['name']} )
    employee_li = employee[0]
    return  employee_li['name']

# Returns User ID from Users table for the supplied Employee ID
def get_user_from_employee(emp_id):
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    resource_id = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['active','=',True],['id','=',emp_id]]], {'fields': ['resource_id']} )
    resource_id_li = resource_id[0]
    user = models.execute_kw(db, sys_uid, sys_password, 'resource.resource', 'search_read', [[['id','=', resource_id_li['resource_id'][0]],]], {'fields': ['user_id']} )
    user_li = user[0]
    #print ("user :  ", user)
    #print ("user_id :  ",user_li['user_id'][0]) 
    return  user_li['user_id'][0]

#Returns employee list 
def emp_list(request):
    empList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    user_id = request.session.get('uid')
    empList = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['active','=',True],]], {'fields': ['name', 'id']} )
    data = json.dumps(empList)
    return HttpResponse(data, content_type='application/javascript' )


# Return all doctors in a system
def doctor_list_simple(request):
    dcrList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    dcrList = models.execute_kw(db, sys_uid, sys_password, 'res.partner', 'search_read', [[['customer','=',True],['doctor','=',True],]], {'fields':['id','name']})
    data = json.dumps(dcrList)
    return HttpResponse(data,content_type='application/javascript')

# Return all products in a system
def product_list(request):
    productList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    productL = models.execute_kw(db, sys_uid, sys_password, 'product.product', 'search_read', [[['active','=',True],['sale_ok','=',True],]],{'fields':['id','name','ppp']})
    for product in productL:
	productList.append({'product_id': product['id'], 'product_name': product['name'], 'ppp': product['ppp']})
    data = json.dumps(productList)
    return HttpResponse(data,content_type='application/javascript')

def mr_list(request):
    mrList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']    
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    user_id = request.session.get('uid')
    resL = models.execute_kw(db, sys_uid, sys_password, 'resource.resource', 'search_read', [[['user_id','=',user_id],]], {'fields': ['id']} ) 
    resli = resL[0] 
    empL = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['active','=',True],['resource_id','=',resli['id']]]], {'fields': ['id']} )
    empli = empL[0]
    mrList_ = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['active','=',True],['parent_id','=',empli['id']]]], {'fields': ['name', 'id']} )
    for mr in mrList_:
    	mrList.append({'mr_id': mr['id'], 'name': mr['name']})
    data = json.dumps(mrList)
    return HttpResponse(data, content_type='application/javascript' )


def asm_list(request):
    asmList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']    
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    user_id = request.session.get('uid')
    hq = request.session.get('hqlist')
    resL = models.execute_kw(db, sys_uid, sys_password, 'resource.resource', 'search_read', [[['user_id','=',user_id],]], {'fields': ['id']} ) 
    resli = resL[0]   
    empL = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['active','=',True],['resource_id','=',resli['id']]]], {'fields': ['name', 'id']} ) 
    data = json.dumps(empL)
    return HttpResponse(data, content_type='application/javascript' )


def hq_list(request):
    hqList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    hqL = models.execute_kw(db, sys_uid, sys_password, 'addsol.region.state', 'search_read', [[[True,'=',True],]], {'fields': ['name', 'id', 'state_id']} )
    for hq in hqL:
	for hqs in request.session['hqlist']:
		if hqs == hq['id']:
			hqList.append({'id': hq['id'], 'name': hq['name'], 'mr_id':get_employee_from_user(get_user_from_HQ(hq['id']))})
    data = json.dumps(hqList)
    return HttpResponse(data,content_type='application/javascript')

def doctor_list(request):
    dcrList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    # get user_id of team in this variable
    user_ids = request.session.get("team_users")
    dcrL = models.execute_kw(db, sys_uid, sys_password, 'res.partner', 'search_read', [[['customer','=',True],['doctor','=',True],['user_id','in',user_ids],]], {'fields':['id','name','user_id'], })
    for dcr in dcrL:
        #for tm in request.session['team']:
        #    empl_id = get_employee_from_user(dcr['user_id'][0])
        empl_id = get_employee_from_user(dcr['user_id'][0])
        #    if tm == empl_id:
		#request.session["doctor_id"] = dcr['id']
                #print 'session id--->',request.session["doctor_id"]
        #        dcrList.append({'id': dcr['id'], 'name': dcr['name'], 'mr_id':empl_id})
        dcrList.append({'id': dcr['id'], 'name': dcr['name'], 'mr_id':empl_id})
				
    data = json.dumps(dcrList)
    return HttpResponse(data,content_type='application/javascript')


def chemist_list(request):
    chemList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    chemL = models.execute_kw(db, sys_uid, sys_password, 'res.partner', 'search_read', [[['customer','=',True],['chemist','=',True],]], {'fields':['id','name','chemist_type','user_id']})
    for chem in chemL:
        #print 'chem----->',chem['id']
    	doc = models.execute_kw(db, sys_uid, sys_password, 'res.partner.doctor.chemist.mapping', 'search_read', [[['chemist_partner_id','=',chem['id']],]], {'fields':['partner_id']})
	if doc:
        	print 'doc----->',doc[0]
		doc_li = doc[0]
    		chemList.append({'id': chem['id'], 'name': chem['name'], 'chemist_type': chem['chemist_type'], 'doctor_id': doc_li['partner_id'][0] })
    data = json.dumps(chemList)
    return HttpResponse(data,content_type='application/javascript')


def state_list(request):
    stateList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    password = settings.GLOBAL_SETTINGS['PASSWORD']
    uid = settings.GLOBAL_SETTINGS['UID']    

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    country_id = models.execute_kw(db, uid, password, 'res.country','search_read', [[['name','=','India'],]], {'fields':['id',]})
    countryli = country_id[0]
    stateList = models.execute_kw(db, uid, password, 'res.country.state', 'search_read', [[['country_id','=',countryli['id']],]])

    data = json.dumps(stateList)
    return HttpResponse(data, content_type='application/javascript' )


def country_list(request):
    countryList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    password = settings.GLOBAL_SETTINGS['PASSWORD']
    uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    countryList = models.execute_kw(db, uid, password, 'res.country','search_read', [[['name','=','India'],]])
    data = json.dumps(countryList)
    return HttpResponse(data,content_type='application/javascript')


def grp_list(request):
    grpList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    password = settings.GLOBAL_SETTINGS['PASSWORD']
    uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    categ_id = models.execute_kw(db, uid, password, 'ir.module.category', 'search_read', [[['name','=','Pharma'],]])
    categli = categ_id[0]
    grpList = models.execute_kw(db, uid, password, 'res.groups', 'search_read', [[['category_id','=',categli['id']],]])
    data = json.dumps(grpList)
    return HttpResponse(data,content_type='application/javascript')


def get_partner_name(part_id):
    partner_id = int(part_id)
    partnerList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    partnerList = models.execute_kw(db, sys_uid, sys_password, 'res.partner', 'search_read', [[['id','=', partner_id],]], {'fields':['id','name']})
    return  partnerList[0]['name']

def get_hq_name(hqp_id):
    hq_id = int(hqp_id)
    hqList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    hqList = models.execute_kw(db, sys_uid, sys_password, 'addsol.region.state', 'search_read', [[['id','=', hq_id],]], {'fields':['id','name']})
    return  hqList[0]['name']

#Returns users list
def user_list(request):
    usrList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    user_id = request.session.get('uid')
    usrList = models.execute_kw(db, sys_uid, sys_password, 'res.users', 'search_read', [[['active','=',True],['invitation','=',False]]], {'fields': ['name', 'id']} )
    data = json.dumps(usrList)
    return HttpResponse(data, content_type='application/javascript' )

