from django.urls import path
from .views import (
  employerLogin_view,
  employerSignUp_view,
  employerHome_view,
  employerProfile_view,
  employerPostJob_view,
  employerJobStatus_view,
  employerApplicants_view,
  employerCreateThreads_view,
  employerListThreads_view,
  employerThreadView,
  employerCreateMessageView,
  employerPricing_view,
  checkOut,
  paymentSuccessful,
  paymentFailed
)

app_name = 'employer'

urlpatterns = [
  path('login/', employerLogin_view, name='employerLogin_view'),
  path('signup/', employerSignUp_view, name='employerSignUp_view'),
  path('home/', employerHome_view, name='employerHome_view'),
  path('profile/', employerProfile_view, name='employerProfile_view'),
  path('post-job/', employerPostJob_view, name='employerPostJob_view'),
  path('jobs-status/', employerJobStatus_view, name='employerJobStatus_view'),
  path('applicants/', employerApplicants_view, name='employerApplicants_view'),
  path('inbox/', employerListThreads_view, name='employerListThreads_view'),
  path('inbox/create-thread/', employerCreateThreads_view, name='employerCreateThreads_view'),
  path('inbox/<int:pk>/', employerThreadView, name='employerThreadView'),
  path('inbox/<int:pk>/create-message/', employerCreateMessageView, name='employerCreateMessageView'),
  path('pricing/', employerPricing_view, name='employerPricing_view'),
  path('checkout/<int:planid>/', checkOut, name='checkOut'),
  path('payment-success/', paymentSuccessful, name='paymentSuccessful'),
  path('payment-failed/', paymentFailed, name='paymentFailed'),
]