from django import forms
from .models import Employee

class EmployeeModelForm(forms.ModelForm):
  class Meta:
    model = Employee
    fields = (
      'location',
      'achievement',
      'phone_no',
      'photo',
      'primary_role',
      'experience',
      'secondary_role',
      'bio',
      'resume',
      'social_profiles',
      'work_experience',
      'education',
      'skills',
      'availability',
    )

class MessageForm(forms.Form):
  message = forms.CharField(label='', max_length=3000)