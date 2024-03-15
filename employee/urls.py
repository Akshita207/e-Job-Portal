from django.urls import path
from .views import (
  employeeLogin_view,
  employeeSignUp_view,
  employeeHome_view,
  employeeProfile_view,
  employeeTrackApplication_view,
  employeeListThreads_view,
  employeeThreadView,
  employeeCreateMessageView
)

app_name = 'employee'

urlpatterns = [
  path('login/', employeeLogin_view, name='employeeLogin_view'),
  path('signup/', employeeSignUp_view, name='employeeSignUp_view'),
  path('home/', employeeHome_view, name='employeeHome_view'),
  path('profile/', employeeProfile_view, name='employeeProfile_view'),
  path('track-applications/', employeeTrackApplication_view, name='employeeTrackApplication_view'),
  path('inbox/', employeeListThreads_view, name='employeeListThreads_view'),
  path('inbox/<int:pk>/', employeeThreadView, name='employeeThreadView'),
  path('inbox/<int:pk>/create-message/', employeeCreateMessageView, name='employeeCreateMessageView'),
]