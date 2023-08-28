from django.contrib import admin
from .models import PreAuthQuery , ClaimQuery
# Register your models here.

admin.site.register(PreAuthQuery)
admin.site.register(ClaimQuery)