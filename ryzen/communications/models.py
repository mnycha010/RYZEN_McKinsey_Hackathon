from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from member.models import Member
from stokvel.models import Stokvel

class CoordinatorMessage(models.Model):
    stokvel = models.ForeignKey(Stokvel, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    target_members = models.ManyToManyField(Member, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username} - {self.message[:20]}"

from django.utils import timezone

class Notification(models.Model):
    CATEGORY_CHOICES = [
        ('payment_reminder', 'Payment Reminder'),
        ('meeting', 'Meeting'),
        ('payout', 'Payout'),
        ('general', 'General'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification to {self.user.username} - {self.title}"
