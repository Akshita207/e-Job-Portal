from django.contrib import admin
from .models import User, ThreadModel, Messages

admin.site.register(User)
admin.site.register(ThreadModel)
admin.site.register(Messages)