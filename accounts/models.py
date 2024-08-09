from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bsl_staff_no = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.user.username

class MeterReading(models.Model):
    # Existing fields...
    staff_id = models.CharField(max_length=100)
    quarter_no = models.CharField(max_length=100)
    current_reading = models.IntegerField()
    previous_reading = models.IntegerField()
    electricity_units = models.IntegerField()
    meter_image = models.ImageField(upload_to='meter_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # New fields for status and rejection reason
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    REJECTION_REASONS = [
        ('incorrect_image', 'Meter image not correct'),
        ('unclear_reading', 'Image reading not clear'),
        ('different_meter', 'Different meter'),
        ('wrong_reading', 'Inserting wrong reading')
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.CharField(max_length=20, choices=REJECTION_REASONS, blank=True, null=True)

    def __str__(self):
        return f"{self.staff_id} - {self.quarter_no}"
