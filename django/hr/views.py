# from django.shortcuts import render

# Create your views here.
try: import simplejson as json
except ImportError: import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from .forms import EmployeeForm
import xmlrpclib
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from datetime import datetime
from django.contrib import messages

#from dateutil.relativedelta import relativedelta

def index(request):
    return render_to_response('hr/index.html', RequestContext(request))

@login_required
def emp(request):
    return render_to_response('hr/emp_list.html', RequestContext(request))

@login_required
def invite(request):
    return render_to_response('hr/invite.html', RequestContext(request))

@login_required
def send_invite(request):
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

    if request.method == "POST":
	user_id = request.POST.get('employee')
	print 'user--->',user_id
	email_id = request.POST.get('emailId')
	invite_flag = True
	print 'flag---->',type(invite_flag)
	html_content = '''Dear Colleagues,

It is with great pleasure that we welcome you to Deltas Pharma.
Your contribution is important to ensure our constant success and growth. We hope that your career will shape up and attain the new heights on professional front.
We ensure that you will get maximum supports from the whole of DELTASIAN.
For further of your on-boarding process, click on below given link.
http://128.199.98.77/hr/join
Once you are done with fulfillment of your personnel information, you are requested to follow further mentioned link for documentation purpose.
www.deltaspharma.com
please do not hesitate to contact Human Resources at any point of time, if required.
Once again, welcome to Deltas Family!
 
Regards,
Corporate Human Resource Team'''
        email = EmailMessage("Invitation Mail", html_content, "deltaspharma@gmail.com", [email_id])
	email.send()
	#models.execute_kw(db, sys_uid , sys_password, 'res.users', 'write', [[user_id], {'login' : 'rupeshg'}])
	messages.add_message(request, messages.SUCCESS, 'Invitation sent successfully')
        return HttpResponseRedirect("/hr/invite")

    return render_to_response('hr/emp_list.html', RequestContext(request))

@login_required
def join(request):
    return render_to_response('hr/emp_list.html', RequestContext(request))

def emp_list(request):
    empList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']    

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.GLOBAL_SETTINGS['URL']))
    user_id = request.session.get('uid')
    empL = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['active','=',True],]], {'fields': ['name', 'id']} )
    for emp in empL:
	for tm in request.session['team']:
                if tm == emp['id']:
			empList.append({'id': emp['id'], 'name': emp['name']})
    data = json.dumps(empList)
    return HttpResponse(data, content_type='application/javascript' ) 

@login_required
def employee_new(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']    

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    if request.method == "POST":
        form = EmployeeForm(request.POST or None)
        #post = form.save(commit=False)
        #post.author = request.user
        #post.published_date = timezone.now()
        #post.save()
        person_name = request.POST.get('empName')
        person_login = request.POST.get('login')
	person_email = request.POST.get('emailId')
	roleid = request.POST.get('grp')
	#groups = []
	role_id = int(roleid)
	if role_id == 69:
            grps = [69,68,67,66,65,64,63]
        elif role_id == 68:
            grps = [68,67,66,65,64,63]
	elif role_id == 67:
	    grps = [67,66,65,64,63]
        elif role_id == 66:
            grps = [66,65,64,63]
        elif role_id == 65:
	    grps = [65,64,63]
        elif role_id == 64:
	    grps = [64,63]
	elif role_id == 63:
	    grps = [63]

	groupid = [(6, 0, grps)]
	person_mobile = request.POST.get('mobile')
        person_street1 = request.POST.get('street1')
        person_street2 = request.POST.get('street2')
	person_city = request.POST.get('city')
	person_state = request.POST.get('state')
	person_zip = request.POST.get('zipCode')
        person_country = request.POST.get('country')
	person_hq = request.POST.get('hq')
	person_mgr = request.POST.get('manager')
	salary = request.POST.get('salary')
	person_da = request.POST.get('da')
	person_ta = request.POST.get('ta')
	doj = request.POST.get('joiningDate')
	probation_date = request.POST.get('probationDate')
	person_dob = request.POST.get('dob')
	person_acc_no = request.POST.get('accountNumber')
	bank_ifsc = request.POST.get('ifscCode')
        bank_name = request.POST.get('bankName')
        #branch_name = request.POST.get('branchName')
	#notes = request.POST.get('notes')

	
        partner_id = models.execute_kw(db, uid , password, 'res.partner', 'create', [{'name' : person_name, 'email' : person_email, 'street' : person_street1, 'street2' : person_street2, 'city' : person_city, 'zip' : person_zip, 'state_id' : person_state, 'country_id' : person_country, 'mobile' : person_mobile, 'customer' : False}])
        user_id = models.execute_kw(db, uid , password, 'res.users', 'create', [{'name' : person_name, 'login' : person_login, 'partner_id' : partner_id, 'region_id' : person_hq, 'groups_id' : groupid}])
        resource_id = models.execute_kw(db, uid , password, 'resource.resource', 'create', [{'name' : person_name, 'user_id' : user_id}])
	bank_id = models.execute_kw(db, uid, password, 'res.bank', 'create', [{'name' : bank_name, 'bic' : bank_ifsc}])
	bank_account_id = models.execute_kw(db, uid, password, 'res.partner.bank', 'create', [{'acc_number' : person_acc_no, 'bank_id' : bank_id}])
        employee_id = models.execute_kw(db, uid , password, 'hr.employee', 'create', [{'name_related' : person_name, 'mobile_phone' : person_mobile, 'work_email' : person_email, 'resource_id' : resource_id, 'parent_id' : person_mgr, 'bank_account_id' : bank_account_id, 'birthday' : person_dob}])
	contract_id = models.execute_kw(db, uid, password, 'hr.contract', 'create', [{'name' : person_name, 'employee_id' : employee_id, 'wage' : salary, 'trial_date_start' : doj, 'trial_date_end' : probation_date}])
	    
        return HttpResponseRedirect("/hr/employee")
        #return redirect('/hr/employee')
    else:
        form = EmployeeForm()
	
    return render(request, 'hr/employee_form_kendo.html', {'form':form})	

@login_required
def hr_policy(request):

   if request.method == "POST":
       return HttpResponseRedirect("/hr/employee_create")

  
   return render_to_response('hr/hrPolicy.html', RequestContext(request))


@login_required
def employee_create(request):
    return render_to_response('hr/employee_form_1.html', RequestContext(request))


def employee_create_process(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

    if request.method == "POST":
	usr_id = request.session.get('uid')
        firstName = request.POST.get('firstName')
        middleName = request.POST.get('middleName')
        lastName = request.POST.get('lastName')
	fullName = str(firstName) +' '+ str(middleName) +' '+ str(lastName)
	birthDate = request.POST.get('birthDate')
        new_birthDate = datetime.strptime(birthDate,'%d/%m/%Y').strftime('%m/%d/%Y')
        birthPlace = request.POST.get('birthPlace')
	birth_state = request.POST.get('state')
	birth_country = request.POST.get('country')
	gender = request.POST.get('gender')
        religion = request.POST.get('religion')
        nationality = request.POST.get('nationality')
	maritalStatus = request.POST.get('maritalStatus')
	marraigeDate = request.POST.get('marraigeDate')
	if maritalStatus=='single':
		new_marraigeDate = '03/31/1900'
	else:
		new_marraigeDate = datetime.strptime(marraigeDate,'%d/%m/%Y').strftime('%m/%d/%Y')
	mother_tongue = request.POST.get('motherTongue')
	resource_id = models.execute_kw(db, uid , password, 'resource.resource', 'create', [{'name' : fullName, 'user_id' : usr_id}])
	employee_id = models.execute_kw(db, uid , password, 'hr.employee', 'create', [{'resource_id' : resource_id, 'name_related' : fullName, 'birthday' : new_birthDate, 'place_of_birth' : birthPlace, 'birth_state_id' : birth_state, 'birth_country_id' : birth_country, 'gender' : gender, 'religion' : religion, 'marital' : maritalStatus, 'mother_tongue' : mother_tongue, 'marraige_date':new_marraigeDate}])
	messages.add_message(request, messages.SUCCESS, 'Employee personal information saved successfully')	
	request.session["new_emp_id"]=int(str(employee_id))


        return HttpResponseRedirect("/hr/employee_address/")

    return render_to_response('hr/employee_form_1.html', RequestContext(request))


@login_required
def employee_address(request):
    return render_to_response('hr/employee_form_2.html', RequestContext(request))


def employee_address_process(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']
    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

    if request.method == "POST":
        careOf = request.POST.get('careOf')
        person_street1 = request.POST.get('street1')
 	person_street2 = request.POST.get('street2')
    	person_city = request.POST.get('city')
    	person_state = int(str(request.POST.get('state')))
    	person_zip = request.POST.get('zipCode')
    	person_country = int(str(request.POST.get('country')))
    	ph_no = request.POST.get('phNo')
    	mobNo = request.POST.get('mobNo')
    
    	careOf_1 = str(request.POST.get('careOf_1'))
    	person_street1_1 = request.POST.get('street1_1')
    	person_street2_1 = request.POST.get('street2_1')
    	person_city_1 = request.POST.get('city_1')
    	person_state_1 = request.POST.get('state_1')
    	person_zip_1 = request.POST.get('zipCode_1')
    	person_country_1 = request.POST.get('country_1')
    	ph_no_1=request.POST.get('phNo_1')
    	mobNo_1 = request.POST.get('mobNo_1')
    
    	careOf_2 = str(request.POST.get('careOf_2'))
    	person_street1_2 = request.POST.get('street1_2')
    	person_street2_2 = request.POST.get('street2_2')
    	person_city_2 = request.POST.get('city_2')
    	person_state_2 = request.POST.get('state_2')
    	person_zip_2 = request.POST.get('zipCode_2')
    	person_country_2 = request.POST.get('country_2')
    	ph_no_2=request.POST.get('phNo_2')
    	mobNo_2 = request.POST.get('mobNo_2')

	partner_id = models.execute_kw(db, uid , password, 'res.users', 'search_read', [[['id','=',request.session['uid']],]], {'fields':['partner_id']})
    	p_id1=partner_id[0]
    	p_id=p_id1['partner_id'][0]

	if len(careOf_1)==0:
        
            models.execute_kw(db, uid , password, 'res.partner', 'write', [[p_id], {'street' : person_street1, 'street2' : person_street2, 'city' : person_city, 'zip' : person_zip, 'state_id' : person_state,'phone':ph_no, 'mobile':mobNo, 'country_id' : person_country}])
        
            u_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name':careOf,'parent_id':p_id,'street' : person_street1, 'street2' : person_street2, 'city' : person_city, 'zip' : person_zip, 'state_id' : person_state, 'country_id' : person_country, 'phone':ph_no, 'mobile':mobNo, 'type':'other'}])
        
            u_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name':careOf,'parent_id':p_id,'street' : person_street1, 'street2' : person_street2, 'city' : person_city, 'zip' : person_zip, 'state_id' : person_state, 'country_id' : person_country, 'phone':ph_no, 'mobile':mobNo, 'type':'other'}])
        
    	elif len(careOf_1)>0 and len(careOf_2)==0:
            models.execute_kw(db, uid , password, 'res.partner', 'write', [[p_id], {'street' : person_street1, 'street2' : person_street2, 'city' : person_city, 'zip' : person_zip, 'state_id' : person_state,'phone':ph_no, 'mobile':mobNo, 'country_id' : person_country}])
        
            u_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name':careOf_1,'parent_id':p_id,'street' : person_street1_1, 'street2' : person_street2_1, 'city' : person_city_1, 'zip' : person_zip_1, 'state_id' : person_state_1, 'country_id' : person_country_1, 'phone':ph_no_1, 'mobile':mobNo_1 ,'type':'other'}])
        
            u_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name':careOf,'parent_id':p_id,'street' : person_street1, 'street2' : person_street2, 'city' : person_city, 'zip' : person_zip, 'state_id' : person_state, 'country_id' : person_country, 'phone':ph_no, 'mobile':mobNo, 'type':'other'}])
        
    	elif len(careOf_2)>0:
            models.execute_kw(db, uid , password, 'res.partner', 'write', [[p_id], {'street' : person_street1, 'street2' : person_street2, 'city' : person_city, 'zip' : person_zip, 'state_id' : person_state,'phone':ph_no, 'mobile':mobNo, 'country_id' : person_country}])
        
            u_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name':careOf_1,'parent_id':p_id,'street' : person_street1_1, 'street2' : person_street2_1, 'city' : person_city_1, 'zip' : person_zip_1, 'state_id' : person_state_1, 'country_id' : person_country_1, 'phone':ph_no_1, 'mobile':mobNo_1 ,'type':'other'}])
        
            u_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name':careOf_2,'parent_id':p_id,'street' : person_street1_2, 'street2' : person_street2_2, 'city' : person_city_2, 'zip' : person_zip_2, 'state_id' : person_state_2, 'country_id' : person_country_2, 'phone':ph_no_2, 'mobile':mobNo_2 ,'type':'other'}])

        messages.add_message(request, messages.SUCCESS, '')

        return HttpResponseRedirect("/hr/employee_education/")

    return render(request, 'hr/employee_form_2.html')



@login_required
def employee_education(request):
    return render_to_response('hr/employee_form_3.html', RequestContext(request))

def emp_edu_details_read(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']    

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    emp_data = models.execute_kw(db, uid, password, 'addsol.employee.education', 'search_read', [[['employee_id','=',request.session['new_emp_id']],]],{'fields':['employee_id','degree','branch','college_name','university_name','from_date','to_date','percentage']})
    data = json.dumps(emp_data)
    return HttpResponse(data,content_type='application/javascript')

def emp_write(request,a):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']    

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    emp_data=a.split(",")
    
        
    emp_data = models.execute_kw(db, uid, password, 'addsol.employee.education', 'create', [{'employee_id':emp_data[0],'degree':emp_data[1],'branch':emp_data[2],'college_name':emp_data[3] ,'university_name':emp_data[4],'from_date':date_formater(emp_data[5],1),'to_date':date_formater(emp_data[6],1),'percentage':emp_data[7]}])
   
    return HttpResponseRedirect("/hr/employee_education/")

def employee_education_process(request):

    if request.method == "POST":
        messages.add_message(request, messages.SUCCESS, '')

        return HttpResponseRedirect("/hr/employee_previous_details/")

    return render(request, 'hr/employee_form_3.html')


@login_required
def employee_previous_details(request):
    return render_to_response('hr/employee_form_4.html', RequestContext(request))

def emp_prev_employer_read(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']    

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    emp_data = models.execute_kw(db, uid, password, 'addsol.previous.employer.details', 'search_read', [[['employee_id','=',request.session['new_emp_id']],]],{'fields':['employee_id','industry' ,'job_title','company_name','city','responsibilities','from_date','to_date','previous_salary']})
    data = json.dumps(emp_data)
    return HttpResponse(data,content_type='application/javascript')

def emp_prev_details_write(request,a):
	
	url = settings.GLOBAL_SETTINGS['URL']
	db = settings.GLOBAL_SETTINGS['DB']
	username = settings.GLOBAL_SETTINGS['USER_NAME']
	password = settings.GLOBAL_SETTINGS['PASSWORD']
	uid = settings.GLOBAL_SETTINGS['UID']
	
	models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
	emp_data=a.split(",")
	
	partner_id = models.execute_kw(db, uid , password, 'res.users', 'search_read', [[['id','=',request.session['uid']],]], {'fields':['partner_id']})
	p_id1=partner_id[0]
	p_id=p_id1['partner_id'][0]
	emp_data = models.execute_kw(db, uid, password, 'addsol.previous.employer.details', 'create', [{'employee_id':emp_data[0],'industry':emp_data[1],'job_title':emp_data[2],'company_name':emp_data[3] ,'city':emp_data[4],'responsibilities':emp_data[5],'from_date':date_formater(emp_data[6],2),'to_date':date_formater(emp_data[7],2),'previous_salary':emp_data[8]}])
    #data = json.dumps(emp_data)
	return HttpResponseRedirect('/hr/employee_previous_details')


def employee_previous_details_process(request):

    if request.method == "POST":
        messages.add_message(request, messages.SUCCESS, '')

        return HttpResponseRedirect("/hr/employee_family_details/")

    return render(request, 'hr/employee_form_4.html')


@login_required
def employee_family_details(request):
    return render_to_response('hr/employee_form_5.html', RequestContext(request))

def emp_family_details_read(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']    

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    emp_data = models.execute_kw(db, uid, password, 'addsol.employee.family.details', 'search_read', [[['employee_id','=',request.session['new_emp_id']],]],{'fields':['employee_id','dob','name','relationship','occupation','personal_emailid']})
    
    
    for index in range(len(emp_data)):
    	fName=emp_data[index]['name'].split()
    	if len(fName)==3:
    		emp_data[index].update(dict(first_name=fName[0]))
    		emp_data[index].update(dict(middle_name=fName[1]))
    		emp_data[index].update(dict(last_name=fName[2]))
    	elif len(fName)==2:
    		emp_data[index].update(dict(first_name=fName[0]))
    		emp_data[index].update(dict(middle_name=fName[1]))
    	elif len(fName)==1:
    		emp_data[index].update(dict(first_name=fName[0]))
    		
    
    data = json.dumps(emp_data)
    return HttpResponse(data,content_type='application/javascript')

def emp_family_details_write(request,a):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    sys_uid = settings.GLOBAL_SETTINGS['UID']    

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    emp_data=a.split(",")

    name=(emp_data[2]+" "+emp_data[3]+" "+emp_data[4])
    emp_data = models.execute_kw(db, sys_uid, sys_password, 'addsol.employee.family.details', 'create', [{'employee_id':emp_data[0],'dob':date_formater(emp_data[1],2),'name':name,'relationship':emp_data[5],'occupation':emp_data[7],'personal_emailid':emp_data[6]}])
    #data = json.dumps(emp_data)
    messages.add_message(request,messages.SUCCESS,'entry added successfully')
    return HttpResponseRedirect('/hr/employee_family_details')


def employee_family_details_process(request):

    if request.method == "POST":
        messages.add_message(request, messages.SUCCESS, '')

        return HttpResponseRedirect("/hr/employee_medical_details/")

    return render(request, 'hr/employee_form_5.html')


@login_required
def employee_medical_details(request):
    return render_to_response('hr/employee_form_6.html', RequestContext(request))


def employee_medical_details_process(request):

    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    sys_uid = settings.GLOBAL_SETTINGS['UID']    

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url)) 

    if request.method == "POST":
        bank_name = request.POST.get('bankName')
        accNo = request.POST.get('acNo')
        branch = request.POST.get('branch')
        ifsc_code = request.POST.get('ifsc')
        pan_no = request.POST.get('pan')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        blood_group = request.POST.get('bloodGroup')
       
        bank_id = models.execute_kw(db, sys_uid, sys_password, 'res.bank', 'create', [{'name' : bank_name, 'bic' : ifsc_code}])
        bank_account_id = models.execute_kw(db, sys_uid, sys_password, 'res.partner.bank', 'create', [{'acc_number' : accNo, 'bank_id' : bank_id}])
        models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'write', [[request.session.get('new_emp_id')], {'bank_account_id' : bank_account_id, 'identification_id' : pan_no, 'height' : height, 'weight' : weight, 'bloodgroup' : blood_group}])

        return HttpResponseRedirect("/hr/employee/")
  
    return render_to_response('hr/employee_form_6.html', RequestContext(request))

def date_formater(date,flag):#for input through calender in kendo to change from friday aug 12 2016 ----> 08/12/2016
    date=date.split()
    if date[1]=='Jan':
        date[1]='01'
    elif date[1]=='Feb':
        date[1]='02'
    elif date[1]=='Mar':
        date[1]='03'
    elif date[1]=='Apr':
        date[1]='04'
    elif date[1]=='May':
        date[1]='05'
    elif date[1]=='Jun':
        date[1]='06'
    elif date[1]=='Jul':
        date[1]='07'
    elif date[1]=='Aug':
        date[1]='08'
    elif date[1]=='Sep':
        date[1]='09'
    elif date[1]=='Oct':
        date[1]='10'
    elif date[1]=='Nov':
        date[1]='11'
    elif date[1]=='Dec':
        date[1]='12'
    if flag==1:
        datef= str(date[1])+"/"+str(01)+"/"+str(date[3])#for mm/yyyy->mm/dd/yyyy
    else:
        datef= str(date[1])+"/"+str(date[2])+"/"+str(date[3])#for mm/dd/yyyy
    print datef," ",type(datef)
    return datef

@login_required
def employee_view_details(request):
	return render(request, 'hr/employee_form_view_1.html')

def employee_view_1(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    emp_data = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['id','=',request.session['emp_id']],]], {'fields':['resource_id', 'name_related', 'birthday', 'place_of_birth', 'birth_state_id', 'birth_country_id', 'gender', 'religion', 'marital', 'mother_tongue', 'marraige_date']})
    if emp_data[0]['marital']=="single":
    	emp_data[0]['marraige_date']="-"
    
    state_name=emp_data[0]['birth_state_id'][1]
    country_name=emp_data[0]['birth_country_id'][1]
    emp_data[0].update({"state":state_name})
    emp_data[0].update({"country":country_name})
    data = json.dumps(emp_data)
    index=1
    return HttpResponse(data,content_type='application/javascript')

def employee_view_2(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    partner_id = models.execute_kw(db, uid , password, 'res.users', 'search_read', [[['id','=',request.session['uid']],]], {'fields':['partner_id']})
    pid= partner_id[0]['partner_id'][0]
    emp_data = models.execute_kw(db, uid , password, 'res.partner', 'search_read', [[['id','=',pid],]], {'fields':['street', 'street2' , 'city' , 'zip' , 'state_id','phone', 'mobile', 'country_id']})
    state_name=emp_data[0]['state_id'][1]
    country_name=emp_data[0]['country_id'][1]
    emp_data[0].update({"state":state_name})
    emp_data[0].update({"country":country_name})
    
    emp_data1 = models.execute_kw(db, uid , password, 'res.partner', 'search_read', [[['parent_id','=',pid],]], {'fields':['street', 'street2' , 'city' , 'zip' , 'state_id','phone', 'mobile', 'country_id']})
    state_name1=emp_data1[0]['state_id'][1]
    country_name1=emp_data1[0]['country_id'][1]
    emp_data1[0].update({"state":state_name1})
    emp_data1[0].update({"country":country_name1})
    emp_data1[1].update({"state":state_name1})
    emp_data1[1].update({"country":country_name1})
    
    data = json.dumps(emp_data+emp_data1)
    
    return HttpResponse(data,content_type='application/javascript')

@login_required
def employee_view_details_2(request):
	return render(request, 'hr/employee_form_view_2.html')

def emp_edu_details_view(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']    

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    emp_data = models.execute_kw(db, uid, password, 'addsol.employee.education', 'search_read', [[['employee_id','=',request.session['emp_id']],]],{'fields':['id','employee_id','degree','branch','college_name','university_name','from_date','to_date','percentage']})
    data = json.dumps(emp_data)
    
    return HttpResponse(data,content_type='application/javascript')

@login_required    
def employee_view_details_3(request):
    return render(request,'hr/employee_form_view_3.html')

def emp_prev_employer_details_view(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']    
    
    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    emp_data = models.execute_kw(db, uid, password, 'addsol.previous.employer.details', 'search_read', [[['employee_id','=',request.session['emp_id']],]],{'fields':['id','employee_id','industry' ,'job_title','company_name','city','responsibilities','from_date','to_date','previous_salary']})
    data = json.dumps(emp_data)
    return HttpResponse(data,content_type='application/javascript')

@login_required    
def employee_view_details_4(request):
    return render(request,'hr/employee_form_view_4.html')

def emp_family_details_view(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']    

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    emp_data = models.execute_kw(db, uid, password, 'addsol.employee.family.details', 'search_read', [[['employee_id','=',request.session['emp_id']],]],{'fields':['id','employee_id','dob','name','firstName','middleName','lastName','relationship','occupation','personal_emailid']})
    
    data = json.dumps(emp_data)
    return HttpResponse(data,content_type='application/javascript')

@login_required
def employee_view_details_5(request):
      return render(request,'hr/employee_form_view_5.html')
    
    
def emp_medical_details_view(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']    

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    emp_data1=models.execute_kw(db, uid, password, 'hr.employee', 'search_read', [[['id','=',request.session['emp_id']],]],{'fields':['bank_account_id','height','weight','bloodgroup']})
    
    data = json.dumps(emp_data1)
    return HttpResponse(data,content_type='application/javascript')

def emp_bank_details_view(request):
    url = settings.GLOBAL_SETTINGS['URL'] 
    db = settings.GLOBAL_SETTINGS['DB'] 
    username = settings.GLOBAL_SETTINGS['USER_NAME'] 
    password = settings.GLOBAL_SETTINGS['PASSWORD'] 
    uid = settings.GLOBAL_SETTINGS['UID']    

    models =xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    emp_data1=models.execute_kw(db, uid, password, 'hr.employee', 'search_read', [[['id','=',request.session['emp_id']],]],{'fields':['bank_account_id','height','weight','bloodgroup']})
    bank_ac_id=emp_data1[0]['bank_account_id'][0]
    emp_data = models.execute_kw(db, uid, password, 'res.partner.bank', 'search_read', [[['id','=',bank_ac_id],]],{'fields':['bank_id','acc_number']})
    acc=emp_data[0]['acc_number']
    
    bank_id=emp_data[0]['bank_id'][0]
   
    emp_data2 = models.execute_kw(db, uid, password, 'res.bank', 'search_read', [[['id','=',bank_id],]],{'fields':['name' , 'bic' ,'street']})
    emp_data2[0].update({"acc":acc})
    data = json.dumps(emp_data2)
    return HttpResponse(data,content_type='application/javascript')
