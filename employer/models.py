from django.db import models
import jsonfield
from user.models import User
from django.contrib.auth.models import BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class EmployerManager(BaseUserManager):
  def get_queryset(self, *args, **kwargs):
    results = super().get_queryset(*args, **kwargs)
    return results.filter(role=User.Role.EMPLOYER)

class EmployerRole(User):
  base_role = User.Role.EMPLOYER
  employer = EmployerManager()
  class Meta:
    proxy = True

@receiver(post_save, sender=EmployerRole)
def create_user_profile(sender, instance, created, **kwargs):
  if created and instance.role == "EMPLOYER":
    Employer.objects.create(user=instance)

class Employer(models.Model):
  id = models.BigAutoField(primary_key=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  photo = models.ImageField(default='avatar.png', upload_to='', blank=True)
  company_address = models.CharField(max_length=300, blank=True)
  company_name = models.CharField(max_length=300, blank=False, default='abc')
  phone_no = models.CharField(max_length=15, blank=False, default='12345')

jobType = [
  ('Full Time', 'Full Time'),
  ('Contract', 'Contract'),
  ('Internship', 'Internship')
]

class Job(models.Model):
  id = models.BigAutoField(primary_key=True)
  employer_id = models.ForeignKey(Employer, to_field='id', on_delete=models.CASCADE)
  title = models.CharField(max_length=150, null=False, blank=False)
  logo = models.ImageField(upload_to='', blank=True)
  company_name = models.CharField(max_length=300, null=False, blank=False)
  location = models.CharField(max_length=150, null=False, blank=False)
  about = models.CharField(max_length=3000, null=False, blank=False)
  qualifications = models.CharField(max_length=3000, blank=True)
  responsibility = models.CharField(max_length=3000, blank=True)
  experience = models.IntegerField(blank=True, null=True, default = 0)
  job_type = models.CharField(max_length=50, blank=True, choices=jobType)
  package = models.CharField(max_length=150, blank=True)
  skills = models.CharField(max_length=350, blank=True)
  status = models.CharField(max_length=50, default="pending", null=False, blank=False)

class Payments(models.Model):
  id = models.BigAutoField(primary_key=True)
  employer_id = models.ForeignKey(Employer, to_field='id', on_delete=models.CASCADE)
  date = models.DateTimeField(blank=False, null=False, default=timezone.now)
  amount = models.IntegerField(blank=False, null=False, default = 0)
  bill = models.FileField(upload_to='', blank=False, null=False, default = None, validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
