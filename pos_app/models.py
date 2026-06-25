from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CashShift(models.Model):
    STATUS_CHOICES = [("open", "Open"), ("closed", "Closed")]

    cashier      = models.ForeignKey(User, on_delete=models.PROTECT, related_name="shifts")
    open_time    = models.DateTimeField(auto_now_add=True)
    close_time   = models.DateTimeField(null=True, blank=True)
    open_amount  = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    close_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    expected_cash= models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    variance     = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    variance_reason = models.TextField(blank=True)
    notes        = models.TextField(blank=True)
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default="open")

    class Meta:
        ordering = ["-open_time"]

    def __str__(self):
        return f"Shift {self.id} — {self.cashier} ({self.status})"


class CashMovement(models.Model):
    MOVEMENT_TYPES = [
        ("sale",    "Sale"),
        ("deposit", "Safe Deposit"),
        ("payout",  "Payout"),
        ("refund",  "Refund"),
    ]
    shift     = models.ForeignKey(CashShift, on_delete=models.CASCADE, related_name="movements")
    type      = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    amount    = models.DecimalField(max_digits=12, decimal_places=2)
    note      = models.TextField(blank=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} KES {self.amount}"
