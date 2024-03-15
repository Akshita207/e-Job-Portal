from django.db import models
import jsonfield
from user.models import User
from django.contrib.auth.models import BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import FileExtensionValidator
from employer.models import Job

class EmployeeManager(BaseUserManager):
  def get_queryset(self, *args, **kwargs):
    results = super().get_queryset(*args, **kwargs)
    return results.filter(role=User.Role.EMPLOYEE)

class EmployeeRole(User):
  base_role = User.Role.EMPLOYEE
  employee = EmployeeManager()
  class Meta:
    proxy = True

@receiver(post_save, sender=EmployeeRole)
def create_user_profile(sender, instance, created, **kwargs):
  if created and instance.role == "EMPLOYEE":
    Employee.objects.create(user=instance)

availabilityType = [
  ('Ready to interview', 'Ready to interview'),
  ('Open to offers', 'Open to offers'),
  ('Closed to offers', 'Closed to offers')
]

class Employee(models.Model):
  id = models.BigAutoField(primary_key=True)
  photo = models.ImageField(default='avatar.png', upload_to='', blank=True)
  location = models.CharField(max_length=200, blank=True)
  achievement = jsonfield.JSONField(blank=True, null=True)
  phone_no = models.CharField(max_length=15, blank=True)
  primary_role = models.CharField(max_length=50, blank=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  experience = models.IntegerField(blank=True, null=True, default = 0)
  secondary_role = models.CharField(max_length=150, blank=True)
  bio = models.CharField(max_length=250, blank=True)
  resume = models.FileField(upload_to='', blank=True, default = None, validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
  social_profiles = jsonfield.JSONField(blank=True, null=True)
  work_experience = jsonfield.JSONField(blank=True, null=True)
  education = jsonfield.JSONField(blank=True, null=True)
  skills = models.CharField(max_length=350, blank=True)
  availability = models.CharField(max_length=50, blank=True, choices=availabilityType)

class JobApplications(models.Model):
  id = models.BigAutoField(primary_key=True)
  employee_id = models.ForeignKey(Employee, to_field='id', on_delete=models.CASCADE)
  job_id = models.ForeignKey(Job, to_field='id', on_delete=models.CASCADE)
  status = models.CharField(max_length=50, default="pending", null=False, blank=False)
