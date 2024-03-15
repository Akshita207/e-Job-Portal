from django import forms
from .models import Employer, Job

class EmployerModelForm(forms.ModelForm):
  class Meta:
    model = Employer
    fields = (
      'photo',
      'phone_no',
      'company_address',
      'company_name'
    )

class JobModelForm(forms.ModelForm):
  class Meta:
    model = Job
    fields = '__all__'
    exclude = ('employer_id', 'status')

class MessageForm(forms.Form):
  message = forms.CharField(label='', max_length=3000)
