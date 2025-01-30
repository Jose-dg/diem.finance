from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

# Existing models (with modifications)

class Credit(models.Model):
    # ... (existing fields)

    # New fields for collection and delinquency tracking
    total_expected_payments = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_received_payments = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    on_time_payments = models.IntegerField(default=0)
    early_payments = models.IntegerField(default=0)
    late_payments = models.IntegerField(default=0)
    days_in_arrears = models.IntegerField(default=0)
    
    # Fields for refinancing and restructuring
    is_refinanced = models.BooleanField(default=False)
    refinance_date = models.DateTimeField(null=True, blank=True)
    
    def calculate_collection_rates(self):
        total_payments = self.on_time_payments + self.early_payments + self.late_payments
        if total_payments > 0:
            self.ctr = (self.total_received_payments / self.total_expected_payments) * 100
            self.on_time_rate = (self.on_time_payments / total_payments) * 100
            self.early_rate = (self.early_payments / total_payments) * 100
        else:
            self.ctr = self.on_time_rate = self.early_rate = 0

    def update_delinquency_status(self):
        if self.days_in_arrears > 30:
            self.is_in_default = True
            if 30 < self.days_in_arrears <= 60:
                self.morosidad_level = 'mild_default'
            elif 60 < self.days_in_arrears <= 90:
                self.morosidad_level = 'moderate_default'
            elif 90 < self.days_in_arrears <= 120:
                self.morosidad_level = 'severe_default'
            else:
                self.morosidad_level = 'critical_default'
        else:
            self.is_in_default = False
            self.morosidad_level = 'on_time'

# New models

class Payment(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    payment_method = models.CharField(max_length=50)  # e.g., 'card', 'transfer', 'crypto'
    is_digital = models.BooleanField(default=False)
    
    PAYMENT_STATUS = [
        ('early', 'Early'),
        ('on_time', 'On Time'),
        ('late', 'Late'),
    ]
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS)

    def save(self, *args, **kwargs):
        if self.payment_date < self.due_date:
            self.status = 'early'
        elif self.payment_date == self.due_date:
            self.status = 'on_time'
        else:
            self.status = 'late'
        super().save(*args, **kwargs)

class DelinquencyManagement(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='delinquency_management')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    recovery_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    management_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    MANAGEMENT_STATUS = [
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('written_off', 'Written Off'),
    ]
    status = models.CharField(max_length=20, choices=MANAGEMENT_STATUS, default='active')

class ClientMetrics(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='metrics')
    credit_utilization_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    lifetime_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    acquisition_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_recurring = models.BooleanField(default=False)
    satisfaction_score = models.IntegerField(null=True, blank=True)  # CSAT score

class CreditApplication(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='credit_applications')
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    purpose = models.TextField()
    application_date = models.DateTimeField(default=timezone.now)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    credit_score = models.IntegerField(null=True, blank=True)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

class Reminder(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='reminders')
    send_date = models.DateTimeField()
    message = models.TextField()
    
    REMINDER_TYPE = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE)
    
    is_sent = models.BooleanField(default=False)
    sent_date = models.DateTimeField(null=True, blank=True)

class EarlyPaymentIncentive(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='early_payment_incentives')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_until = models.DateTimeField()
    is_claimed = models.BooleanField(default=False)

class FinancialMetrics(models.Model):
    date = models.DateField(unique=True)
    total_loans_outstanding = models.DecimalField(max_digits=15, decimal_places=2)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2)
    net_income = models.DecimalField(max_digits=15, decimal_places=2)
    default_rate = models.DecimalField(max_digits=5, decimal_places=2)
    recovery_rate = models.DecimalField(max_digits=5, decimal_places=2)
    average_loan_term = models.IntegerField()  # in days
    average_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def calculate_metrics(self):
        # Logic to calculate various financial metrics
        pass
