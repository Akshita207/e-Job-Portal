from django.shortcuts import render, redirect
from .models import EmployerRole, Employer, Job, Payments
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import EmployerModelForm, JobModelForm, MessageForm
from employee.models import Employee, JobApplications
from itertools import chain
from user.models import ThreadModel, Messages, User
from django.db.models import Q
from instamojo_wrapper import Instamojo
from django.conf import settings
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime, timedelta, timezone
from django.urls import reverse
import urllib.parse

api = Instamojo(
  api_key = settings.API_KEY,
  auth_token = settings.AUTH_TOKEN,
  endpoint = 'https://test.instamojo.com/api/1.1/'
)

paymentResponse = None

def employerLogin_view(request):
  if request.user.is_authenticated:
    return render(request, 'emp-home.html')
  if request.method == 'POST':
    name = request.POST.get('name')
    password = request.POST.get('pass')
    user = authenticate(username=name, password=password)
    if user is not None and user.role == 'EMPLOYER':
      login(request, user)
      return redirect('employer:employerHome_view')
    else:
      messages.error(request,'Email or password is incorrect.')
      return redirect('employer:employerLogin_view')
  return render(request, 'emp-login.html')

def employerSignUp_view(request):
  if request.user.is_authenticated:
    return render(request, 'emp-home.html')
  if request.method == 'POST':
    ename = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    company = request.POST.get('company')
    phone = request.POST.get('phone')
    emp = EmployerRole.objects.create_user(username=ename, email=email, password=password)
    empObj = Employer.objects.filter(user=emp).first()
    empObj.company_name = company
    empObj.phone_no = phone
    empObj.save()
    return redirect('employer:employerLogin_view')
  return render(request, 'emp-signup.html')

@login_required
def employerHome_view(request):
  if request.user.role == 'EMPLOYER':
    emp = Employee.objects.all()
    form_data = {}
    if request.method == 'POST':
      d1 = Employee.objects.all()
      form_data = request.POST.dict()
      if (form_data['name']):
        d1 = d1.filter(user__username__icontains=form_data['name'])
      if form_data['experience']:
        d1 = d1.filter(experience=form_data['experience'])
      if form_data['skills']:
        d1 = d1.filter(skills__icontains=form_data['skills'])
      emp = d1
    context = {
      'emp': emp,
      'formData': form_data
    }
    return render(request, 'emp-home.html', context)

@login_required
def employerProfile_view(request):
  if request.user.role == 'EMPLOYER':
    employer = Employer.objects.filter(user=request.user).first()
    form = EmployerModelForm(request.POST or None, request.FILES or None, instance=employer)
    confirm = False
    confirmError = ''

    if request.method == 'POST':
      if form.is_valid():
        form.save()
        confirm = True
        confirmError = ''
      else:
        confirmError = form.errors
    
    context = {
      'employer': employer,
      'form': form,
      'confirm': confirm,
      'confirmError': confirmError
    }
    return render(request, 'emp-profile.html', context)

@login_required
def employerPostJob_view(request):
  if request.user.role == 'EMPLOYER':
    employer = Employer.objects.filter(user=request.user).first()
    form = JobModelForm(request.POST or None, request.FILES or None)
    confirm = False
    confirmError = ''
    payment = Payments.objects.filter(employer_id=employer.id)
    allowedPosts = 0
    today = datetime.now(timezone.utc)
    jobs = Job.objects.filter(employer_id=employer.id, status='approved')
    for p in payment:
      date = p.date + timedelta(days=30)
      date = date.replace(tzinfo=timezone.utc)
      if date >= today:
        if p.amount == 400:
          allowedPosts += 6 
        elif p.amount == 800:
          allowedPosts += 20

    if allowedPosts == 0:
      allowedPosts = 2

    if request.method == 'POST':
      if form.is_valid():
        f = form.save(commit=False)
        f.employer_id_id = employer.id
        f.save()
        form = JobModelForm()
        confirm = True
        confirmError = ''
      else:
        confirmError = form.errors
    
    context = {
      'form': form,
      'confirm': confirm,
      'confirmError': confirmError,
      'allowedPosts': allowedPosts,
      'jobs': jobs
    }
    return render(request, 'emp-postJob.html', context)

@login_required
def employerJobStatus_view(request):
  if request.user.role == 'EMPLOYER':
    emp = Employer.objects.filter(user=request.user).first()
    jobs = Job.objects.filter(employer_id=emp.id)
    confirm = False
    confirmError = ''

    if request.method == 'POST':
      form_data = request.POST.dict()
      if form_data['submit']:
        try:
          Job.objects.filter(id=form_data['submit']).delete()
          jobs = Job.objects.filter(employer_id=emp.id)
          confirm = True
          confirmError = ''
        except Exception as e:
          confirmError = e

    context = {
      'jobs': jobs,
      'confirm': confirm,
      'confirmError': confirmError
    }
    return render(request, 'emp-jobs-status.html', context)

@login_required
def employerApplicants_view(request):
  if request.user.role == 'EMPLOYER':
    confirm = False
    confirmError = ''
    if request.method == 'POST':
      try:
        form_data = request.POST.dict()
        if form_data['submit']:
          idList = form_data['submit'].split(',')
          instance = JobApplications.objects.filter(employee_id = idList[0], job_id = idList[1]).first()
          instance.status = idList[2]
          instance.save()
          confirm = True
          confirmError = ''
          if idList[2] == 'accepted':
            msgTo = Employee.objects.filter(id=idList[0]).first()
            url = '{}?{}'.format(reverse('employer:employerCreateThreads_view'), urllib.parse.urlencode({'messageTo': msgTo.user}))
            return redirect(url)
      except Exception as e:
        confirmError = e

    emp = Employer.objects.filter(user=request.user).first()
    jobs = Job.objects.filter(employer_id=emp.id, status='approved')
    ids = list(jobs.values_list('id', flat=True))
    resultList = []
    for j in jobs:
      obj = {'job': j}
      arr = []
      application = JobApplications.objects.filter(job_id=j.id, status='pending')
      applicationIds = list(application.values_list('employee_id', flat=True))
      for a in applicationIds:
        employee = Employee.objects.filter(id=a).first()
        arr.append(employee)
      obj['applicant'] = arr
      resultList.append(obj)

    context = {
      'jobApplicantList': resultList,
      'confirm': confirm,
      'confirmError': confirmError,
    }
    return render(request, 'emp-applicants.html', context)

@login_required
def employerListThreads_view(request):
  if request.user.role == 'EMPLOYER':
    threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
    context = {
      'threads': threads
    }
    return render(request, 'emp-inbox.html', context)

@login_required
def employerCreateThreads_view(request):
  if request.user.role == 'EMPLOYER':
    form_data = {}
    if request.method == 'POST':
      form_data = request.POST.dict()
    if request.method == 'GET':
      form_data = request.GET.dict()
    if form_data['messageTo']:
      receiver = User.objects.get(username=form_data['messageTo'])
      if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
        thread = ThreadModel.objects.filter(user=request.user, receiver=receiver).first()
        return redirect('employer:employerThreadView', pk=thread.pk)
      elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
        thread = ThreadModel.objects.filter(user=receiver, receiver=request.user).first()
        return redirect('employer:employerThreadView', pk=thread.pk)
      thread = ThreadModel(
        user=request.user,
        receiver=receiver
      )
      thread.save()
      return redirect('employer:employerThreadView', pk=thread.pk)

@login_required
def employerThreadView(request, pk):
  if request.user.role == 'EMPLOYER':
    form = MessageForm()
    thread = ThreadModel.objects.get(pk=pk)
    messageList = Messages.objects.filter(thread__pk__contains=pk)
    context = {
      'thread': thread,
      'form': form,
      'messageList': messageList
    }
    return render(request, 'emp-social-thread.html', context)

@login_required
def employerCreateMessageView(request, pk):
  if request.user.role == 'EMPLOYER':
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
    return redirect('employer:employerThreadView', pk=pk)

@login_required
def employerPricing_view(request):
  return render(request, 'emp-pricing.html')

@login_required
def checkOut(request, planid):
  if request.user.role == 'EMPLOYER':
    host = request.get_host()
    plan = {
      'name': 'Free',
      'price': 0,
      'id': planid,
      'description': ['2 Active Posts']
    }
    price = 0
    if (planid == 1):
      price = 400
      plan['price'] = 400
      plan['name'] = 'Basic'
      plan['description'] = ['6 Active Posts']
    elif (planid == 2):
      price = 800
      plan['price'] = 800
      plan['name'] = 'Pro'
      plan['description'] = ['20 Active Posts']
    
    response = api.payment_request_create(
      amount = price,
      purpose = 'Order Process',
      buyer_name = request.user,
      email = request.user.email,
      redirect_url = 'http://127.0.0.1:8000/employer/payment-success/'
    )
    print(response)
    global paymentResponse
    paymentResponse = {
      'date': response['payment_request']['created_at'],
      'plan': plan
    }
    context = {
      'plan': plan,
      'payment_url': response['payment_request']['longurl']
    }
    return render(request, 'emp-checkout.html', context)

@login_required
def paymentSuccessful(request):
  if request.user.role == 'EMPLOYER':
    global paymentResponse
    emp = Employer.objects.filter(user=request.user).first()
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    entry0 = 'Name: ' + str(request.user)
    entry1 = 'Plan: ' + paymentResponse['plan']['name']
    entry2 = 'Amount: ' + str(paymentResponse['plan']['price'])
    entry3 = 'Date: ' + str(datetime.strptime(paymentResponse['date'], "%Y-%m-%dT%H:%M:%S.%fZ"))
    p.drawString(100, 650, entry3)
    p.drawString(100, 700, entry2)
    p.drawString(100, 750, entry1)
    p.drawString(100, 800, entry0)
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    payment = Payments(
      employer_id_id = emp.id,
      date = paymentResponse['date'],
      amount = paymentResponse['plan']['price']
    )
    payment.bill.save('bill.pdf', ContentFile(pdf))
    payment.save()
    paymentResponse = {}
    return render(request, 'emp-payment-success.html')

@login_required
def paymentFailed(request):
  if request.user.role == 'EMPLOYER':
    return render(request, 'emp-payment-failed.html')