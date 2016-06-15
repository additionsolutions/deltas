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
from .forms import PPPForm, PPPForm_2, PPPRecordForm, PPPRecordAmount
import xmlrpclib
from django.contrib.auth.decorators import login_required
from django.db import connections
from datetime import datetime
from base64 import b64encode
from io import TextIOWrapper
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import  helper

def index(request):
    #return HttpResponse("Hello, world. You're at the Deltas Marketing site.")
    return render_to_response('marketing/index.html', RequestContext(request))

@login_required
def ppp(request):
    if not messages.get_messages(request):
    	messages.add_message(request, messages.INFO, 'Use button below to add new PPP record')
    return render_to_response('marketing/ppplist.html', RequestContext(request))


def ppplist(request):
    pppList = []
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']
 
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    #pppList = models.execute_kw(db, sys_uid, sys_password, 'addsol.ppp', 'search_read', [[['asm_id','=',request.session['uid']],]])
    pppL = models.execute_kw(db, sys_uid, sys_password, 'addsol.ppp', 'search_read', [[[True,'=', True],]], {'fields':['id','asm_id','ppp_date','region_id','mr_id','partner_id','mode','status']} )
    pppRL = models.execute_kw(db, sys_uid, sys_password, 'addsol.ppp.record.line', 'search_read',[[[True,'=',True],]],{'fields':['addsol_ppp_id','record_amount']})
    for pppLd in pppL:
	amount_sum = 0
	count = 0
	for ids in pppRL:
            if ids['addsol_ppp_id'][0]== pppLd['id']:
                amount_sum = amount_sum + ids['record_amount']
                count += 1
	for tm in request.session['team']:
		if tm == pppLd['asm_id'][0]:
    			pppList.append({'id': pppLd['id'], 'date': pppLd['ppp_date'], 'hq': pppLd['region_id'][1], 'mr': pppLd['mr_id'][1], 'doctor': pppLd['partner_id'][1], 'payment_mode': pppLd['mode'], 'status': pppLd['status'], 'amount': amount_sum, 'count': count})

    data = json.dumps(pppList)
    return HttpResponse(data, content_type='application/javascript' )

@login_required
def ppp_new(request):
    return render_to_response('marketing/ppp_form.html', RequestContext(request))

@login_required
def ppp_new_2(request, ppp):
    try:
        ppp = int(ppp)
    except ValueError:
        raise Http404()
    return render_to_response('marketing/ppp_form_2.html', RequestContext(request,{'ppp': ppp}))


def ppp_new_process(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

    if request.method == "POST":
        form = PPPForm(request.POST or None)
        ppp_date = request.POST.get('pppDate')
	new_date = datetime.strptime(ppp_date,'%d/%m/%Y').strftime('%m/%d/%Y')
        ppp_mode = request.POST.get('mode')
        asm_id = request.POST.get('asm')
        mr_id = request.POST.get('mr')
	partner_id = request.POST.get('customer')
	hq_id = request.POST.get('hq')
	ppp_id = models.execute_kw(db, uid , password, 'addsol.ppp', 'create', [{'ppp_date' : new_date, 'mode' : ppp_mode, 'asm_id' : asm_id, 'mr_id' : mr_id, 'partner_id' : partner_id, 'region_id' : hq_id, 'status' : 'Submitted'}])
	# Save values in session variables to send in email after step 2
	request.session['doctor_name'] = helper.views.get_partner_name(int(partner_id))
	request.session['hq_name'] = helper.views.get_hq_name(int(hq_id))
        return HttpResponseRedirect("/mktg/ppp_new_2/" + str(ppp_id))
    else:
        form = PPPForm()

    return render(request,'marketing/ppp_form.html', {'form':form})    

def pppline(request, ppp):
    try:
        ppp = int(ppp)
    except ValueError:
        raise Http404()
    pppLine = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    pppLineList = models.execute_kw(db, sys_uid, sys_password, 'addsol.ppp.line', 'search_read', [[['addsol_ppp_id','=',ppp],]], {'fields':['id','product_id','expected_quantity','expected_amount']})
    for pppl in pppLineList:
    	pppLine.append({'pppLineID':pppl['id'] , 'product_id': pppl['product_id'][0], 'product_name': pppl['product_id'][1], 'expected_quantity': pppl['expected_quantity'], 'expected_amount': pppl['expected_amount']})
	
    data = json.dumps(pppLine)
    return HttpResponse(data,content_type='application/javascript')

def ppp_new_process_2(request, ppp):
    try:
        ppp = int(ppp)
    except ValueError:
        raise Http404()

    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    list_prod = []
    if request.method == "POST":
        form = PPPForm_2(request.POST or None)
	#product_ids = request.POST.get('product_ids')
        nature = request.POST.get('nature')
        period = request.POST.get('period') 
	comment = request.POST.get('comment')
        amount = request.POST.get('totalAmount')
        allowance_nature = request.POST.get('allowanceNature')
	other = request.POST.get('other')
        allowance_percentage = request.POST.get('allowancePercentage')
        promotional_allowance = float(amount) * float(allowance_percentage)
        remark = request.POST.get('remark')
	products = request.POST.get('sel_products')
        
        list_prod = products.split(",")        
        #print 'listroducts--->',list_prod
        for prod in list_prod:
            #print 'product ---->',prod
            ppp_line_id = models.execute_kw(db, sys_uid, sys_password, 'addsol.ppp.line', 'create',[{'addsol_ppp_id' : ppp, 'product_id' : prod, 'expected_quantity' : 0, 'expected_amount' : 0}])


        models.execute_kw(db, sys_uid , sys_password, 'addsol.ppp', 'write', [[ppp], {'nature' : nature, 'period' : period, 'period_comment' : comment,'total_expected_amount' : amount, 'allowance_nature' : allowance_nature, 'nature_comment' : other, 'promotional_allowance' : promotional_allowance, 'allowance_percentage' : allowance_percentage, 'remark' : remark, 'status' : 'Submitted'}])
	# email settings
	msg_plain = render_to_string('emails/ppp_email.txt', {'asm': request.session['user_name'], 'amount': amount, 'allowance': promotional_allowance, 'period': period})
	msg_html = render_to_string('emails/ppp_email.html', {'asm': request.session['user_name'], 'hq': request.session['hq_name'], 'doctor': request.session['doctor_name'], 'amount': amount, 'allowance': promotional_allowance, 'period': period})
        #email = EmailMessage('PPP Created', body, to=[settings.GLOBAL_SETTINGS['TO_PPP']])
	#email.send()
	send_mail(
    		'PPP Created',
    		msg_plain,
    		'deltaspharma@gmail.com',
    		[settings.GLOBAL_SETTINGS['TO_PPP']],
    		html_message=msg_html,
	)

    	messages.add_message(request, messages.SUCCESS, 'PPP record saved successfully')
	return HttpResponseRedirect("/mktg/ppp" )
    else:
        form = PPPForm_2()

    return render(request,'marketing/ppp_form.html', {'form':form})

@login_required
def pppApprove(request):
    role = request.session['role'] 
    if role == 'ASM' or role == 'MR':
	return render_to_response('message.html', {'message':'ALERT: You do not have access right for this function. Please contact System Administrator'})
	
    return render_to_response('marketing/ppplist.html', RequestContext(request))


def ppp_list_approve(request):
    pppListApprove = []
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    #pppList = models.execute_kw(db, sys_uid, sys_password, 'addsol.ppp', 'search_read', [[['asm_id','=',request.session['uid']],]])
    pppLA = models.execute_kw(db, sys_uid, sys_password, 'addsol.ppp', 'search_read', [[[True,'=', True],]], {'fields':['id','asm_id','ppp_date','region_id','mr_id','partner_id','promotional_allowance','total_expected_amount','status']} )
    for pppLd in pppLA:
        for tm in request.session['team']:
                if tm == pppLd['asm_id'][0]:
                        pppListApprove.append({'id': pppLd['id'], 'date': pppLd['ppp_date'], 'hq': pppLd['region_id'][1], 'mr': pppLd['mr_id'][1], 'doctor': pppLd['partner_id'][1], 'promotional_allowance': pppLd['promotional_allowance'],'expected_amount': pppLd['total_expected_amount'], 'status': pppLd['status']})

    data = json.dumps(pppListApprove)
    return HttpResponse(data, content_type='application/javascript' )

def ppp_approve(request, appId):
    try:
        appId = int(appId)
    except ValueError:
        raise Http404()

    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    models.execute_kw(db, sys_uid , sys_password, 'addsol.ppp', 'write', [[appId], {'status' : 'Approved'}])
    return HttpResponseRedirect("/mktg/pppApprove")


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
	#file = request.FILES['files']
        #bytes = files.read()
        #output = str.decode(files)
	#if files:
        #img_data = file.read()  #b64encode(file)
        #print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        #print file #data---->',bytes

	ppp_record_id = models.execute_kw(db, sys_uid, sys_password, 'addsol.ppp.records', 'create', [{'record_date' : new_recordDate, 'partner_id' : partner_id, 'asm_id' : asm, 'mr_id' : mr, 'amount' : amount}])
    	messages.add_message(request, messages.SUCCESS, 'PPP bill record added successfully')
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


@csrf_exempt    
def ppp_record_amount(request):
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']
    
    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    if request.method == "POST":
        form= PPPRecordAmount(request.POST,request.FILES)
        pppId = request.POST.get('pppId')
        if form.is_multipart() and ('files' in request.FILES):
            save_file(request.FILES['files'], pppId+'_' )
        
        amount = request.POST.get('amount')
        record=models.execute_kw(db, sys_uid, sys_password, 'addsol.ppp.record.line', 'create', [{'addsol_ppp_id' : pppId,'record_amount' : amount}])
	#Send email with file as attachment
	html_content = "This is mail body in HTML"
	email = EmailMessage("PPP Bill", html_content, "deltaspharma@gmail.com", ["dilip.jain@deltaspharma.com"] )	
	#email.attach('ppp_file.png',request.FILES['files'],'image/png')
	#email.attach(attachment.name, attachment.read(), attachment.content_type)
	if 'files' in request.FILES:
	    attachment = request.FILES['files'] 
            email.attach_file(settings.MEDIA_ROOT+'/'+pppId+'_'+attachment.name)
	    email.send()
    	messages.add_message(request, messages.SUCCESS, 'PPP bill record added successfully')
        return HttpResponseRedirect("/mktg/ppp")
    else:
        form = pppRecordAmount()

      
    return render_to_response(request, 'marketing/ppplist.html',{'form':form})
    

# To save uploaded files
def save_file(file, path=''):
   ''' Little helper to save a file
   '''
   filename = file._get_name()
   fd = open('%s/%s' % (settings.MEDIA_ROOT, str(path) + str(filename)), 'wb')
   for chunk in file.chunks():
       fd.write(chunk)
   fd.close()


