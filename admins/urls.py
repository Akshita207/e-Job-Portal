from django.urls import path
from .views import (
  adminsLogin_view,
  adminsHome_view,
  adminsManageJob_view,
  adminsManageEmployee_view,
  adminsManageEmployer_view
)

app_name = 'admins'

urlpatterns = [
  path('login/', adminsLogin_view, name='adminsLogin_view'),
  path('home/', adminsHome_view, name='adminsHome_view'),
  path('manage-jobs/', adminsManageJob_view, name='adminsManageJob_view'),
  path('manage-employees/', adminsManageEmployee_view, name='adminsManageEmployee_view'),
  path('manage-employers/', adminsManageEmployer_view, name='adminsManageEmployer_view'),
]