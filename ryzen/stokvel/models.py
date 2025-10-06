from django.db import models
from django.utils import timezone
from member.models import Member

class Stokvel(models.Model):
    """
    Stokvel entity created by admin only.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    monthly_contribution = models.DecimalField(max_digits=12, decimal_places=2)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
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

    # Admin of the stokvel
    admin = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_stokvels"
    )

    def total_members(self):
        return self.members.count()

    def __str__(self):
        return f"{self.name} ({self.total_members()} members)"
