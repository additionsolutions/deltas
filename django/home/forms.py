from django import forms

class LoginForm(forms.Form):
	user = forms.CharField()
	password = forms.CharField()


class ContactForm(forms.Form):
   subject = forms.CharField()
   email_to = forms.EmailField()
   message = forms.CharField(
       
       widget=forms.Textarea
   )
