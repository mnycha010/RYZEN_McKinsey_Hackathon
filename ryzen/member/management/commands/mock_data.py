from django.core.management.base import BaseCommand
from django.utils import timezone
from member.models import Member, FinancialRecord
from datetime import timedelta
import random

class Command(BaseCommand):
    help = "Generate mock financial data for dashboard charts"

    def handle(self, *args, **kwargs):
        members = Member.objects.all()
        if not members.exists():
            self.stdout.write(self.style.ERROR("No members found. Please create members first."))
            return

        today = timezone.now().date()
        for member in members:
            for month_offset in range(6, 0, -1):  # Last 6 months
                first_day_of_month = today.replace(day=1) - timedelta(days=month_offset*30)
                # Create 4 records per month (weekly)
                for week in range(4):
                    contribution_date = first_day_of_month + timedelta(days=week*7)
                    amount_saved = random.uniform(100, 1000)
                    amount_borrowed = random.uniform(50, 500)

                    FinancialRecord.objects.create(
                        member=member,
                        amount_saved=round(amount_saved, 2),
                        amount_borrowed=round(amount_borrowed, 2),
                        contribution_date=contribution_date,
                        notes="Mock data for dashboard charts"
                    )

        self.stdout.write(self.style.SUCCESS("Mock financial data generated for all members!"))
