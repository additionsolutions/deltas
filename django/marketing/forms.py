from django import forms
#from .models import Employee
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
#from crispy_forms.bootstrap import FormActions

class PPPForm(forms.Form):
	pppDate = forms.DateField()
	mode = forms.CharField()
	asm = forms.IntegerField()
	mr = forms.IntegerField()   
	hq = forms.IntegerField()
	customer = forms.IntegerField()
	#product = forms.IntegerField()
	#quantity = forms.IntegerField()
	#price = forms.DecimalField()
	#product1 = forms.IntegerField()
	#quantity1 = forms.IntegerField()
	#price1 = forms.DecimalField()
	#product2 = forms.IntegerField()
	#quantity2 = forms.IntegerField()
	#price2 = forms.DecimalField()
	#nature = forms.CharField()
	#totalAmount = forms.DecimalField()
        #period = forms.CharField()
	#promotionalAllowance = forms.CharField()
	#allowanceNature = forms.CharField()
	#remark = forms.CharField()
	
class PPPForm_2(forms.Form):
        #product = forms.IntegerField()
        #product1 = forms.IntegerField()
        #product2 = forms.IntegerField()
	product_ids = forms.CharField()
        nature = forms.CharField()
        totalAmount = forms.DecimalField()
        period = forms.CharField()
        promotionalAllowance = forms.CharField()
        allowanceNature = forms.CharField()
        remark = forms.CharField()


class PPPRecordForm(forms.Form):
	recordDate = forms.DateField()

class PPPRecordAmount(forms.Form):
    	pppId = forms.IntegerField()
    	amount = forms.DecimalField()
	files = forms.FileField()
