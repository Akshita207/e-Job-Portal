from django.contrib import admin
from .models import Employer, Job, Payments

admin.site.register(Employer)
admin.site.register(Job)
admin.site.register(Payments)