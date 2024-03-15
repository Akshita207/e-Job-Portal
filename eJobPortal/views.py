from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout

def home_view(request):
  if request.user.is_authenticated:
    if request.user.role == 'EMPLOYEE':
      return render(request, 'home.html')
    if request.user.role == 'EMPLOYER':
      return render(request, 'emp-home.html')
    if request.user.role == 'ADMIN':
      return render(request, 'adm-home.html')
  return render(request, 'index.html')

def logoutUser(request):
  logout(request)
  return render(request, 'index.html')