from django.contrib import admin
from .models import Court, UserProfile, Judge, Case, CaseType, TimeLine

# Register your models here.
admin.site.register(Court)
admin.site.register(UserProfile)
admin.site.register(Judge)
admin.site.register(Case)
admin.site.register(CaseType)
admin.site.register(TimeLine)
