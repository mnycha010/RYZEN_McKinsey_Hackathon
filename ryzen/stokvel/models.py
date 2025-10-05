from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member")
    
    # Extra properties
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    stokvel = models.ForeignKey("stokvel.Group", on_delete=models.SET_NULL, blank=True, null=True, related_name="members")

    def __str__(self):
        return self.user.username


class Stokvel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    monthly_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Interest rate (optional)")
    payout_cycle = models.CharField(
        max_length=50,
        choices=[
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
            ("annual", "Annual"),
            ("custom", "Custom"),
        ],
        default="monthly",
    )
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    # Relationships
    admin = models.ForeignKey(
        "user.Member",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_stokvels"
    )

    members = models.ManyToManyField(
        "user.Member",
        related_name="joined_stokvels",
        blank=True,
    )

    def total_contributions(self):
        """Returns the total amount contributed by all members."""
        return sum(member.contribution_set.aggregate(models.Sum("amount"))["amount__sum"] or 0 for member in self.members.all())

    def total_members(self):
        return self.members.count()

    def __str__(self):
        return f"{self.name} ({self.total_members()} members)"

