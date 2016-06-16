# from django.shortcuts import render

# Create your views here.
try: import simplejson as json
except ImportError: import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from .forms import LoginForm
import xmlrpclib
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import helper
from django.core.mail import EmailMessage

def index(request):
    return render_to_response('index.html', RequestContext(request))

@login_required
def mpage(request):
    return render_to_response('home/mpage.html', RequestContext(request))


@login_required
def contact(request):
    return render_to_response('home/contact.html', RequestContext(request))

@login_required
def help(request):
    return render_to_response('home/help.html', RequestContext(request))

def intra_login(request):
    if request.user.is_authenticated():
        template = loader.get_template('home/resp.html')
	user = request.session.get('role')
        context = {'uid': user}
        return HttpResponse(template.render(context, request))
	#return HttpResponseRedirect('/home/resp.html')
    else:
	return render_to_response('home/emp_login.html', RequestContext(request))

def login_process(request):
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    sys_password = settings.GLOBAL_SETTINGS['PASSWORD']
    sys_uid = settings.GLOBAL_SETTINGS['UID']

    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    template = loader.get_template('home/resp.html')
    next_url = ""

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('user')
            upassword = request.POST.get('password')
            next_url = request.POST.get('next')
            uid = common.authenticate(db, username, upassword, {})
            if uid:
		##authenticate : This is default user is created in Django DB
                user = authenticate(username='abcdefghgfedcba', password='!Qazx78mnb+*&tyu521#')
		login(request, user)
                #context = {'uid': user}
                #return HttpResponse(template.render(context, request))
		# Set values in session
		request.session['uid']=uid
		request.session['user_name']=helper.views.get_employee_name_from_user(uid)
		
		models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
		# Set role in session
		# List Records
		groups = models.execute_kw(db, sys_uid, sys_password,'res.groups', 'search_read',[[['users', '=', uid] ]],{'fields': ['id','name',]})
		# Set marketing role as 'role'
		a = 1
		for item in groups:
        		for id in item:
                		if item[id]==59:
                        		a = 1000000 + a
                		elif item[id]==58:
                        		a = 100000 + a
                		elif item[id]==57:
                        		a = 10000 + a
                		elif item[id]==56:
                        		a = 1000 + a
                		elif item[id]==55:
                        		a = 100 + a
                		elif item[id]==54:
                        		a = 10 + a
                		elif item[id]==53:
                        		a = 1 + a
                		else:
                        		a = a
		if a==1111112:
        		request.session['role']="Director"
		elif a==111112:
        		request.session['role']="GM"
		elif a==11112:
        		request.session['role']="DGM"
		elif a==1112:
        		request.session['role']="ZSM"
		elif a==112:
        		request.session['role']="RSM"
		elif a==12:
        		request.session['role']="ASM"
		elif a==2:
        		request.session['role']="MR"
		elif a==1:
        		request.session['role']="None"			
		# --- End of marketing role --- #

		# Set HR role as 'hr_role'
		b = 1
		for item in groups:
        		for id in item:
                		if item[id]==51:  # HR Manager
        				b = 10 + b
                		elif item[id]==50: # Officer
                        		b = 1 + b
				elif item[id]==4:  # Employee
        				b = b 
		if b==12:
        		request.session['hr_role']="Manager"
		elif b==2:
        		request.session['hr_role']="Officer"
		elif b==1:
        		request.session['hr_role']="Employee"			
               # ---- End of HR role --- # 

		# Set team in session
		team = []
		empl0 = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['user_id', '=', uid] ]], {'fields': ['name','id']})	
		if empl0:
			empl0d = empl0[0]
			request.session["emp_id"]=empl0d['id']
			team.append(empl0d['id'])
			empl1 = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['parent_id', '=', empl0d['id']] ]], {'fields': ['name','id']})		
			if empl1:
				for emp1 in empl1:
					empl2 = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['parent_id', '=', emp1['id']] ]], {'fields':['name','id']})
                			team.append(emp1['id'])
                			if not empl2:
                        			continue
					for emp2 in empl2:
                        			empl3 = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['parent_id', '=', emp2['id']] ]], {'fields':['name','id']})
                        			team.append(emp2['id'])
                        			if not empl3:
                                			continue
						for emp3 in empl3:
                                			empl4 = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['parent_id', '=', emp3['id']] ]], {'fields':['name','id']})
                                			team.append(emp3['id'])
                                			if not empl4:
                                        			continue
							for emp4 in empl4:
                                        			empl5 = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['parent_id', '=', emp4['id']] ]], {'fields':['name','id']})
                                        			team.append(emp4['id'])
                                        			if not empl5:
                                                 			continue
								for emp5 in empl5:
                                                			empl6 = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['parent_id', '=', emp5['id']] ]], {'fields':['name','id']})
                                                			team.append(emp5['id'])
                                                			if not empl6:
										continue
									for emp6 in empl6:
                                                    				empl7 = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['parent_id', '=', emp6['id']] ]], {'fields':['name','id']})
                                                    				team.append(emp6['id'])
                                                    				if not empl7:
                                                        				continue
		else:
        		print "Top Boss- No Parent"
		
		#if team_h:
		#	team_h = team_h + "}"
		request.session['team'] = team
		# --- End of team --- #

		# Build team with user_id from res.users table #
		team_users = []
		for member in team:
			usr = helper.views.get_user_from_employee(member)
			team_users.append(usr)
		request.session['team_users'] = team_users
		# ---- End of team_users --- #

		# Set allowed hqlist in session #
		hqlist = []
		for member in team:
        		emp = models.execute_kw(db, sys_uid, sys_password, 'hr.employee', 'search_read', [[['id', '=', member] ]], {'fields':['resource_id',]})
			if emp:
				empd = emp[0]
				empli = empd['resource_id']
        			res = models.execute_kw(db, sys_uid, sys_password, 'resource.resource', 'search_read', [[['id', '=', empli[0]]]], {'fields':['user_id',]})
				if res:
					resd =  res[0] 
					resli = resd['user_id']
        				hq = models.execute_kw(db, sys_uid, sys_password, 'res.users', 'search_read', [[['id', '=', resli[0]] ]], {'fields':['region_id',]})
        				for hqeach in hq :
						if hqeach['region_id']:
							hqlist.append(hqeach['region_id'][0])
		request.session['hqlist']=hqlist
		# --- End of hqlist --- #
		
		if next_url == "":
                    return HttpResponseRedirect('/home/mpage')
                else:
                    return HttpResponseRedirect(next_url)
		#return HttpResponseRedirect('home/mpage')
        else:
            form = LoginForm()
    auth_message = "ERROR: Invalid username and/or password. Try Again!!"
    context = {'auth_message': auth_message}
    return render_to_response('home/emp_login.html', context, RequestContext(request))
    #return render(RequestContext(request), 'home/emp_login.html')


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def intra_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

def user_hq_list(request):
    hqList = []
    url = settings.GLOBAL_SETTINGS['URL']
    db = settings.GLOBAL_SETTINGS['DB']
    username = settings.GLOBAL_SETTINGS['USER_NAME']
    password = settings.GLOBAL_SETTINGS['PASSWORD']
    uid = settings.GLOBAL_SETTINGS['UID']

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    hqlist = models.execute_kw(db, uid, password, 'addsol.res.users', 'search_read', [[[id,'=',request.session.get('uid')],]])
    data = json.dumps(hqlist)
    return HttpResponse(data,content_type='application/javascript')

def send_mail(request):
    
    url = settings.GLOBAL_SETTINGS['URL']
    it=settings.GLOBAL_SETTINGS['TO_IT']
    hr=settings.GLOBAL_SETTINGS['TO_HR']
    ppp=settings.GLOBAL_SETTINGS['TO_PPP']
    mktg=settings.GLOBAL_SETTINGS['TO_MARKETING']
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    if request.method == 'POST':
        if request.POST.get('email_to')=='HR':
            email_to = hr
        elif request.POST.get('email_to')=='IT':
            email_to = it
        elif request.POST.get('email_to')=='PPP':
            email_to = ppp
        else : email_to = mktg    
        
        subject = request.POST.get('subject')
        
        message = request.POST.get('message')
        
        email = EmailMessage(subject, message, "deltaspharma@gmail.com",[email_to] )
        email.send()
	return HttpResponseRedirect("/")
                
    return render_to_response('home/contact.html')
