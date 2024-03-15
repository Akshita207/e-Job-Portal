from django import forms
from employee.models import Employee, JobApplications
from employer.models import Employer, Job

class EmployerModelForm(forms.ModelForm):
  class Meta:
    model = Employer
    fields = '__all__'

class JobModelForm(forms.ModelForm):
  class Meta:
    model = Job
    fields = '__all__'

class EmployeeModelForm(forms.ModelForm):
  class Meta:
    model = Employee
    fields = '__all__'

class JobApplicationsModelForm(forms.ModelForm):
  class Meta:
    model = JobApplications
    fields = '__all__'