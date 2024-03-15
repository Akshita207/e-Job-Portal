from django.db import models
from user.models import User

class Admin(models.Model):
  id = models.BigAutoField(primary_key=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
