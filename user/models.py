from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
  class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    EMPLOYEE = "EMPLOYEE", "Employee"
    EMPLOYER = "EMPLOYER", "Employer"

  base_role = Role.ADMIN

  role = models.CharField(max_length=50, choices=Role.choices)

  def save(self, *args, **kwargs):
    if not self.pk:
      self.role = self.base_role
      return super().save(*args, **kwargs)

class ThreadModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class Messages(models.Model):
  id = models.BigAutoField(primary_key=True)
  thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE, blank=True, null=True)
  from_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
  to_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
  description = models.CharField(max_length=3000)
  date = models.DateTimeField(default=timezone.now)

