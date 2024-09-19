from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('donor', 'Donor'),
        ('recipient', 'Recipient'),
        ('admin', 'Administrator'),
    )

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    blood_group = models.CharField(
        max_length=3, blank=True, null=True)
    location = models.CharField(max_length=255)
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default='recipient')

    badges = models.ManyToManyField('Badge', blank=True)
    stars = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username


class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='blood_requests', limit_choices_to={'user_type': 'recipient'}
    )
    requested_blood_group = models.CharField(max_length=3)
    request_date = models.DateTimeField(default=timezone.now)
    urgency = models.CharField(
        max_length=20, choices=[('Immediate', 'Immediate'), ('24 hours', 'Within 24 hours'), ('3 days', 'Within 3 days'), ('7 days', 'Within 7 days')]
    )
    location = models.CharField(max_length=255)
    additional_info = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='pending'
    )

    fulfilled_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='fulfilled_requests'
    )

    def __str__(self):
        return f"Blood request by {self.recipient.username} for {self.requested_blood_group} at {self.location}"


class BloodDonation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='donations', limit_choices_to={'user_type': 'donor'})
    date_of_donation = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=255)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                  blank=True, related_name='received_blood')
    is_verified = models.BooleanField(
        default=False)

    blood_request = models.OneToOneField(
        BloodRequest, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Donation by {self.donor.username} on {self.date_of_donation}"

    @staticmethod
    def can_donate(donor):
        """
        Check if a donor is eligible to donate blood again (must wait 3 months between donations).
        """
        last_donation = BloodDonation.objects.filter(
            donor=donor).order_by('-date_of_donation').first()
        if last_donation:
            time_since_last_donation = timezone.now() - last_donation.date_of_donation
            return time_since_last_donation >= timedelta(days=90)
        return True


class Badge(models.Model):
    # e.g., '5 Donations', 'Life Saver'
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='badges/icons/', blank=True, null=True)
    # Number of donations needed to earn this badge
    threshold = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} on {self.timestamp}"


class BloodInventory(models.Model):
    blood_group = models.CharField(max_length=3)
    available_units = models.PositiveIntegerField(
        default=0)
    last_updated = models.DateTimeField(auto_now=True)
    hospital_location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.blood_group} - {self.available_units} units"


class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='campaign_images/', blank=True, null=True)

    def __str__(self):
        return self.title



class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')  # Image upload field

    def __str__(self):
        return f"Image {self.id}"  # This returns the image ID when converted to string
