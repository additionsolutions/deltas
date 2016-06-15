from django import forms
#from .models import Employee
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
#from crispy_forms.bootstrap import FormActions

class EmployeeForm(forms.Form):
	empName = forms.CharField()
	login = forms.CharField()
	emailId = forms.CharField()
	grp = forms.IntegerField()
	mobile = forms.CharField()   
	street1 = forms.CharField()
	street2 = forms.CharField()
	city = forms.CharField()
	zipCode = forms.CharField()
	state = forms.IntegerField()
        country = forms.IntegerField()
	hq = forms.IntegerField()
	manager = forms.IntegerField()
	salary = forms.DecimalField()
	da = forms.DecimalField()
	ta = forms.DecimalField()
	joiningDate = forms.DateField()
	probationDate = forms.DateField()
	dob = forms.DateField()
        accountNumber = forms.CharField()
	ifscCode = forms.CharField()
        bankName = forms.CharField()
        #branchName = forms.CharField()
	#notes = forms.TextField()

