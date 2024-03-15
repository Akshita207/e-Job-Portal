from django.shortcuts import render, redirect
from .models import EmployeeRole, Employee, JobApplications
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import EmployeeModelForm, MessageForm
from employer.models import Job
from itertools import chain
from user.models import ThreadModel, Messages, User
from django.db.models import Q
from django.shortcuts import redirect

def employeeLogin_view(request):
  if request.user.is_authenticated:
    return render(request, 'home.html')
  if request.method == 'POST':
    name = request.POST.get('name')
    password = request.POST.get('pass')
    user = authenticate(username=name, password=password)

    if user is not None and user.role == 'EMPLOYEE':
      login(request, user)
      return redirect('employee:employeeHome_view')
    else:
      messages.error(request,'Email or password is incorrect.')
      return redirect('employee:employeeLogin_view')
  return render(request, 'login.html')

def employeeSignUp_view(request):
  if request.user.is_authenticated:
    return render(request, 'home.html')
  if request.method == 'POST':
    ename = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    emp = EmployeeRole.objects.create_user(username=ename, email=email, password=password)
    return redirect('employee:employeeLogin_view')
  return render(request, 'signup.html')

@login_required
def employeeHome_view(request):
  if request.user.role == 'EMPLOYEE':
    jobs = Job.objects.all()
    employee = Employee.objects.filter(user=request.user).first()
    confirm = False
    confirmError = ''
    form_data = {}
    if request.method == 'POST':
      form_data = request.POST.dict()
      if len(form_data) > 1 and 'title' in form_data :
        d1 = Job.objects.all()
        if (form_data['title']):
          d1 = d1.filter(title__icontains=form_data['title'])
        if (form_data['company']):
          d1 = d1.filter(company_name__icontains=form_data['company'])
        if form_data['experience']:
          d1 = d1.filter(experience=form_data['experience'])
        if (form_data['package']):
          d1 = d1.filter(package__icontains=form_data['package'])
        if form_data['location']:
          d1 = d1.filter(location__icontains=form_data['location'])
        jobs = d1
      else:
        if form_data['submit']:
          try:
            instance = JobApplications(employee_id_id = employee.id, job_id_id = form_data['submit'], status = 'pending')
            instance.save()
            confirm = True
            confirmError = ''
          except Exception as e:
            confirmError = e
    
    appliedJobsObj = JobApplications.objects.filter(employee_id=employee.id)
    appliedJobs = list(appliedJobsObj.values_list('job_id', flat=True))

    context = {
      'jobs': jobs,
      'appliedJobs': appliedJobs,
      'confirm': confirm,
      'confirmError': confirmError,
      'formData': form_data
    }
    return render(request, 'home.html', context)

@login_required
def employeeProfile_view(request):
  if request.user.role == 'EMPLOYEE':
    employee = Employee.objects.filter(user=request.user).first()
    form = EmployeeModelForm(request.POST or None, request.FILES or None, instance=employee)
    confirm = False
    confirmError = ''

    if request.method == 'POST':
      form_data = request.POST.dict()
      if (len(form_data) > 0):
        socialProfileObj = {
          'website': form_data['website'],
          'github': form_data['github'],
          'linkedIn': form_data['linkedIn'],
          'twitter': form_data['twitter']
        }
        workObj = []
        educationObj = []
        achievementObj = []
        for m in form_data:
          if m.startswith('achievement') and len(form_data[m]) > 0:
            achievementObj.append({m: form_data[m]})
          if m.startswith('wrk') and len(form_data[m]) > 0:
            prefix, suffix, number = m.split("-")
            if (len(workObj) <= (int(number))):
              while (len(workObj) <= (int(number))):
                workObj.append({})
            workObj[int(number)][m] = form_data[m]
          if m.startswith('ed') and len(form_data[m]) > 0:
            prefix2, suffix2, number2 = m.split("-")
            if (len(educationObj) <= (int(number2))):
              while (len(educationObj) <= (int(number2))):
                educationObj.append({})
            educationObj[int(number2)][m] = form_data[m]
        try:
          employee.location = form_data['location']
          employee.achievement = achievementObj
          employee.phone_no = form_data['phone_no']
          employee.primary_role = form_data['primary_role']
          employee.experience = form_data['experience']
          employee.secondary_role = form_data['secondary_role']
          employee.bio = form_data['bio']
          employee.social_profiles = socialProfileObj
          employee.work_experience = workObj
          employee.education = educationObj
          employee.skills = form_data['skills']
          employee.availability = form_data['availability']
          if request.FILES.get('resume'):
            employee.resume = request.FILES.get('resume')
          if request.FILES.get('photo'):
            employee.photo = request.FILES.get('photo')
          employee.save()
          confirm = True
          confirmError = ''
        except Exception as e:
          confirmError = e
    
    context = {
      'employee': employee,
      'confirm': confirm,
      'confirmError': confirmError
    }
    return render(request, 'profile.html', context)

@login_required
def employeeTrackApplication_view(request):
  if request.user.role == 'EMPLOYEE':
    emp = Employee.objects.filter(user=request.user).first()
    confirm = False
    confirmError = ''

    if request.method == 'POST':
      form_data = request.POST.dict()
      if form_data['submit']:
        try:
          JobApplications.objects.filter(employee_id=emp.id, job_id=form_data['submit']).delete()
          confirm = True
          confirmError = ''
        except Exception as e:
          confirmError = e

    appliedJobsObj = JobApplications.objects.filter(employee_id=emp.id)
    ids = list(appliedJobsObj.values_list('job_id', flat=True))
    status = list(appliedJobsObj.values_list('status', flat=True))
    jobs = []
    for i in ids:
      job = Job.objects.filter(id=i).first()
      jobs.append(job)

    job_status = zip(jobs, status)

    context = {
      'jobs': job_status,
      'confirm': confirm,
      'confirmError': confirmError
    }

    return render(request, 'track-application.html', context)

@login_required
def employeeListThreads_view(request):
  if request.user.role == 'EMPLOYEE':
    threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
    context = {
      'threads': threads
    }
    return render(request, 'inbox.html', context)

@login_required
def employeeThreadView(request, pk):
  if request.user.role == 'EMPLOYEE':
    form = MessageForm()
    thread = ThreadModel.objects.get(pk=pk)
    messageList = Messages.objects.filter(thread__pk__contains=pk)
    context = {
      'thread': thread,
      'form': form,
      'messageList': messageList
    }
    return render(request, 'social-thread.html', context)

@login_required
def employeeCreateMessageView(request, pk):
  if request.user.role == 'EMPLOYEE':
    thread = ThreadModel.objects.get(pk=pk)
    if thread.receiver == request.user:
      receiver = thread.user
    else:
      receiver = thread.receiver

    message = Messages(
      thread=thread,
      from_id=request.user,
      to_id=receiver,
      description=request.POST.get('message')
    )
    message.save()
    return redirect('employee:employeeThreadView', pk=pk)
