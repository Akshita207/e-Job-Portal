from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from employer.models import Employer, Job
from employee.models import Employee
from .forms import JobModelForm, EmployeeModelForm, EmployerModelForm

def adminsLogin_view(request):
  if request.user.is_authenticated:
    return render(request, 'adm-home.html')
  if request.method == 'POST':
    name = request.POST.get('name')
    password = request.POST.get('pass')
    user = authenticate(username=name, password=password)
    if user is not None and user.role == 'ADMIN':
      login(request, user)
      return redirect('admins:adminsHome_view')
    else:
      messages.error(request,'Email or password is incorrect.')
      return redirect('admins:adminsLogin_view')
  return render(request, 'adm-login.html')

@login_required
def adminsHome_view(request):
  if request.user.role == 'ADMIN':
    jobs = Job.objects.filter(status='pending')
    confirm = False
    confirmError = ''
    if request.method == 'POST':
      form_data = request.POST.dict()
      if form_data['submit']:
        try:
          idList = form_data['submit'].split(',')
          instance = Job.objects.filter(id = idList[0]).first()
          instance.status = idList[1]
          instance.save()
          jobs = Job.objects.filter(status='pending')
          confirm = True
          confirmError = ''
        except Exception as e:
          confirmError = e
    context = {
      'confirm': confirm,
      'confirmError': confirmError,
      'jobs': jobs
    }
    return render(request, 'adm-home.html', context)

@login_required
def adminsManageJob_view(request):
  if request.user.role == 'ADMIN':
    confirm = ''
    confirmError = ''

    if request.method == 'POST':
      form_data = request.POST.dict()
      if len(form_data) == 2:
        if form_data['delete']:
          try:
            Job.objects.filter(id=int(form_data['delete'])).delete()
            confirm = 'Job deleted successfully.'
            confirmError = ''
          except Exception as e:
            confirm = ''
            confirmError = e
      if len(form_data) > 2:
        if form_data['jobid']:
          job = Job.objects.get(id=int(form_data['jobid']))
          formInstance = JobModelForm(request.POST or None, request.FILES or None, instance=job)
          if formInstance.is_valid():
            formInstance.save()
            confirm = 'Job updated successfully'
            confirmError = ''
          else:
            confirmError = form.errors
      
    jobs = Job.objects.all()
    jobObj = []
    for j in jobs:
      if request.method == 'POST' and len(form_data) > 2 and str(j.id) == form_data['jobid']:
        job = Job.objects.get(id=int(form_data['jobid']))
        form = JobModelForm(request.POST or None, request.FILES or None, instance=job)
      else:
        form = JobModelForm(instance=j)
      jobObj.append({
        'job': j,
        'form': form
      })

    context = {
      'jobs': jobObj,
      'confirm': confirm,
      'confirmError': confirmError,
    }

    return render(request, 'adm-manage-job.html', context)

@login_required
def adminsManageEmployee_view(request):
  if request.user.role == 'ADMIN':
    confirm = ''
    confirmError = ''

    if request.method == 'POST':
      form_data = request.POST.dict()
      if len(form_data) == 2:
        if form_data['delete']:
          try:
            Employee.objects.filter(id=int(form_data['delete'])).delete()
            confirm = 'Employee deleted successfully.'
            confirmError = ''
          except Exception as e:
            confirm = ''
            confirmError = e
      if len(form_data) > 2:
        if form_data['employeeid']:
          employee = Employee.objects.get(id=int(form_data['employeeid']))
          formInstance = EmployeeModelForm(request.POST or None, request.FILES or None, instance=employee)
          if formInstance.is_valid():
            formInstance.save()
            confirm = 'Employee updated successfully'
            confirmError = ''
          else:
            confirmError = form.errors
      
    emps = Employee.objects.all()
    empObj = []
    for e in emps:
      if request.method == 'POST' and len(form_data) > 2 and str(e.id) == form_data['employeeid']:
        employee = Employee.objects.get(id=int(form_data['employeeid']))
        form = EmployeeModelForm(request.POST or None, request.FILES or None, instance=employee)
      else:
        form = EmployeeModelForm(instance=e)
      empObj.append({
        'employee': e,
        'form': form
      })

    context = {
      'employees': empObj,
      'confirm': confirm,
      'confirmError': confirmError,
    }

    return render(request, 'adm-manage-employee.html', context)

@login_required
def adminsManageEmployer_view(request):
  if request.user.role == 'ADMIN':
    confirm = ''
    confirmError = ''

    if request.method == 'POST':
      form_data = request.POST.dict()
      if len(form_data) == 2:
        if form_data['delete']:
          try:
            Employer.objects.filter(id=int(form_data['delete'])).delete()
            confirm = 'Employer deleted successfully.'
            confirmError = ''
          except Exception as e:
            confirm = ''
            confirmError = e
      if len(form_data) > 2:
        if form_data['employerid']:
          employer = Employer.objects.get(id=int(form_data['employerid']))
          formInstance = EmployerModelForm(request.POST or None, request.FILES or None, instance=employer)
          if formInstance.is_valid():
            formInstance.save()
            confirm = 'Employer updated successfully'
            confirmError = ''
          else:
            confirmError = form.errors
      
    emps = Employer.objects.all()
    empObj = []
    for e in emps:
      if request.method == 'POST' and len(form_data) > 2 and str(e.id) == form_data['employerid']:
        employer = Employer.objects.get(id=int(form_data['employerid']))
        form = EmployerModelForm(request.POST or None, request.FILES or None, instance=employer)
      else:
        form = EmployerModelForm(instance=e)
      empObj.append({
        'employer': e,
        'form': form
      })

    context = {
      'employers': empObj,
      'confirm': confirm,
      'confirmError': confirmError,
    }

    return render(request, 'adm-manage-employer.html', context)