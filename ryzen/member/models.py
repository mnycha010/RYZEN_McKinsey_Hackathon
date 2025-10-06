from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Member(models.Model):
    """
    Extends the default Django User with additional profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    # Optional link to a stokvel
    stokvel = models.ForeignKey(
        "stokvel.Stokvel",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="members"
    )

    def __str__(self):
        return self.user.username


class FinancialRecord(models.Model):
    """
    Tied to a Member; stores individual financial information.
    """
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="financial_records")
    amount_saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    amount_borrowed = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    contribution_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.member.user.username} - {self.amount_saved} saved"


