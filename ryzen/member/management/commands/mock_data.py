import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from member.models import Member, FinancialRecord
from stokvel.models import Stokvel

class Command(BaseCommand):
    help = "Creates mock users, members, stokvels, and financial records"

    def handle(self, *args, **kwargs):
        # --- Create Stokvels ---
        stokvels_data = [
            {"name": "Alpha Stokvel", "monthly_contribution": 100, "target_amount": 5000},
            {"name": "Beta Stokvel", "monthly_contribution": 150, "target_amount": 8000},
            {"name": "Gamma Stokvel", "monthly_contribution": 200, "target_amount": 10000},
        ]

        stokvels = []
        for s in stokvels_data:
            stokvel, created = Stokvel.objects.get_or_create(
                name=s["name"],
                defaults={
                    "monthly_contribution": s["monthly_contribution"],
                    "target_amount": s["target_amount"],
                    "admin": None,  # assign later if needed
                }
            )
            stokvels.append(stokvel)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created stokvel: {stokvel.name}"))

        # --- Create Users & Members ---
        for i in range(1, 6):
            username = f"user{i}"
            email = f"user{i}@example.com"
            password = "password123"

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=password)
                stokvel = random.choice(stokvels)
                member = Member.objects.create(
                    user=user,
                    phone_number=f"08200000{i}",
                    address=f"123 Mock St, City {i}",
                    date_of_birth="1990-01-01",
                    stokvel=stokvel
                )
                stokvel.members.add(member)

                FinancialRecord.objects.create(
                    member=member,
                    amount_saved=random.randint(100, 1000),
                    amount_borrowed=random.randint(0, 500)
                )

                self.stdout.write(self.style.SUCCESS(f"Created user/member: {username}, joined {stokvel.name}"))

        self.stdout.write(self.style.SUCCESS("✅ Mock data created successfully!"))
