from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.conf import settings
#from django.utils import simplejson
try: import simplejson as json
except ImportError: import json
from marketing.models import PPP
from marketing.models import Product
from .forms import PPPForm, PPPRecordForm
import xmlrpclib
from django.contrib.auth.decorators import login_required
from django.db import connections
from datetime import datetime

def index(request):
    #return HttpResponse("Hello, world. You're at the Deltas Marketing site.")
    return render_to_response('marketing/index.html', RequestContext(request))

@login_required
def ppp(request):
    #return HttpResponse("Hello, world. You're at the ppp index.")
    return render_to_response('marketing/ppplist.html', RequestContext(request))


def ppplist(request):
    pppList = []
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']
 
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    #pppList = models.execute_kw(db, sys_uid, sys_password, 'addsol.ppp', 'search_read', [[['asm_id','=',request.session['uid']],]])
    pppL = models.execute_kw(db, sys_uid, sys_password, 'addsol.ppp', 'search_read', [[[True,'=', True],]], {'fields':['asm_id','ppp_date','region_id','mr_id','partner_id','mode','status']} )
    for pppLd in pppL:
	for tm in request.session['team']:
		if tm == pppLd['asm_id'][0]:
    			pppList.append({'date': pppLd['ppp_date'], 'hq': pppLd['region_id'][1], 'mr': pppLd['mr_id'][1], 'doctor': pppLd['partner_id'][1], 'payment_mode': pppLd['mode'], 'status': pppLd['status']})

    data = json.dumps(pppList)
    return HttpResponse(data, content_type='application/javascript' )

def doctor_list(request):
    dcrList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    password = settings.GLOBAL_SETTINGS['PASSWORD']
    uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    dcrList = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['customer','=',True],['doctor','=',True],]], {'fields':['id','name']})
    data = json.dumps(dcrList)
    return HttpResponse(data,content_type='application/javascript')


def product_list(request):
    productList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    password = settings.GLOBAL_SETTINGS['PASSWORD']
    uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    productList = models.execute_kw(db, uid, password, 'product.product', 'search_read', [[['active','=',True],['sale_ok','=',True],]],{'fields':['id','name',]})
    data = json.dumps(productList)
    return HttpResponse(data,content_type='application/javascript')

@login_required
def ppp_new(request):
    #return HttpResponse("Hello, world. You're at the ppp index.")
    return render_to_response('marketing/ppp_form.html', RequestContext(request))


def ppp_new_process(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

    if request.method == "POST":
        form = PPPForm(request.POST or None)
        #post = form.save(commit=False)
        #post.author = request.user
        #post.published_date = timezone.now()
        #post.save()
        ppp_date = request.POST.get('pppDate')
	new_date = datetime.strptime(ppp_date,'%d/%m/%Y').strftime('%m/%d/%Y')
        ppp_mode = request.POST.get('mode')
        asm_id = request.POST.get('asm')
        mr_id = request.POST.get('mr')
	partner_id = request.POST.get('customer')
	hq_id = request.POST.get('hq')
	nature = request.POST.get('nature')
	totalAmount = request.POST.get('totalAmount')
	period = request.POST.get('period')
	promotionalAllowance = request.POST.get('promotionalAllowance')
	allowanceNature = request.POST.get('allowanceNature')
	remark = request.POST.get('remark')
	product_id = request.POST.get('product')
	quantity = request.POST.get('quantity')
	price = request.POST.get('price')
	product_id1 = request.POST.get('product1')
	quantity1 = request.POST.get('quantity1')
        price1 = request.POST.get('price1')
	product_id2 = request.POST.get('product2')
	quantity2 = request.POST.get('quantity2')
	price2 = request.POST.get('price2')
	ppp_id = models.execute_kw(db, uid , password, 'addsol.ppp', 'create', [{'ppp_date' : new_date, 'mode' : ppp_mode, 'asm_id' : asm_id, 'mr_id' : mr_id, 'partner_id' : partner_id, 'region_id' : hq_id, 'nature' : nature, 'total_expected_amount' : totalAmount, 'period' : period, 'promotional_allowance' : promotionalAllowance, 'allowance_nature' : allowanceNature, 'remark' : remark, 'status' : 'submit'}])
	ppp_line_id = models.execute_kw(db, uid, password, 'addsol.ppp.line', 'create',[{'addsol_ppp_id' : ppp_id, 'product_id' : product_id, 'expected_quantity' : quantity, 'expected_amount' : price}])
	ppp_line_id = models.execute_kw(db, uid, password, 'addsol.ppp.line', 'create',[{'addsol_ppp_id' : ppp_id, 'product_id' : product_id1, 'expected_quantity' : quantity1, 'expected_amount' : price1}])
	ppp_line_id = models.execute_kw(db, uid, password, 'addsol.ppp.line', 'create',[{'addsol_ppp_id' : ppp_id, 'product_id' : product_id2, 'expected_quantity' : quantity2, 'expected_amount' : price2}])
        return HttpResponseRedirect("/mktg/ppp")
        #return redirect('/hr/employee')
    else:
        form = PPPForm()

    return render(request,'marketing/ppp_form.html', {'form':form})    

@login_required
def pppRecord(request):
    #return HttpResponse("Hello, world. You're at the ppp index.")
    return render_to_response('marketing/pppRecord_list.html')


def pppRecord_list(request):
    pppRecordList = []
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))

    pppRL = models.execute_kw(db, sys_uid, sys_password, 'addsol.ppp.records', 'search_read', [[[True,'=', True],]], {'fields':['record_date','asm_id','mr_id','amount']} )
    
    for pppRLd in pppRL:
	for tm in request.session['team']:
		if tm == pppRLd['asm_id'][0]:
    			pppRecordList.append({'date': pppRLd['record_date'], 'mr': pppRLd['mr_id'][1], 'amount': pppRLd['amount']})



    data = json.dumps(pppRecordList)
    return HttpResponse(data, content_type='application/javascript' )

@login_required
def ppp_new_record(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url)) 
    
    if request.method == "POST":
	recordDate = request.POST.get('recordDate')
	new_recordDate = datetime.strptime(recordDate,'%d/%m/%Y').strftime('%m/%d/%Y')
	partner_id = request.POST.get('customerId')
	asm = request.POST.get('asmId')
	mr = request.POST.get('mrId')
	amount = request.POST.get('amount')
	files = request.FILES
        #print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        #print files

	ppp_record_id = models.execute_kw(db, sys_uid, sys_password, 'addsol.ppp.records', 'create', [{'record_date' : new_recordDate, 'partner_id' : partner_id, 'asm_id' : asm, 'mr_id' : mr, 'amount' : amount}])
	return HttpResponseRedirect("/mktg/pppRecord")
    else:
	form = PPPRecordForm()

    return render(request,'marketing/ppp_records.html')

def ppp_line(request):
    #return HttpResponse("Hello, world. You're at the ppp index.")
    return render_to_response('marketing/ppp_line_form.html', RequestContext(request))

@login_required
def ppp_report_data(request):
    #return HttpResponse("Hello, world. You're at the ppp index.")
    return render_to_response('marketing/ppp_report_data.html')


# Return results as dictionary
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def ppp_data(request):
    sqlData = []
    emp_list_id = request.session.get('team')
    emp_ids = tuple(emp_list_id)
    sql_stmt = """SELECT rtrim(to_char(ppp_date,'Month')) as month_name,sum(total_expected_amount) as amount 
				FROM addsol_ppp 
             	WHERE asm_id IN """ + str(emp_ids) + """ GROUP BY month_name UNION SELECT rtrim(to_char(record_date,'Month')) as month_name,sum(amount) as amount 
				FROM addsol_ppp_records 
             	WHERE asm_id IN """ + str(emp_ids) + """ GROUP BY month_name"""
    # Take data from odoo table
    cursor = connections['odoo_data'].cursor()
    cursor.execute(sql_stmt)
    #row = cursor.fetchall()
    sqlData = dictfetchall(cursor)
    data = json.dumps(sqlData)
    return HttpResponse(data, content_type='application/javascript' )
