from django.contrib import admin
from .models import Member, FinancialRecord

# Register Member
admin.site.register(Member)

# Register FinancialRecord
admin.site.register(FinancialRecord)
