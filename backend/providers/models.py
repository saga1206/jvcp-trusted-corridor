from django.db import models
from django.contrib.auth.models import User

class Provider(models.Model):
    CATEGORY_CHOICES = [
        ('hotel', 'Hotel'),
        ('homestay', 'Homestay'),
        ('restaurant', 'Restaurant'),
        ('tour_guide', 'Tour Guide'),
        ('travel_agency', 'Travel Agency'),
        ('experience', 'Local Experience'),
        ('merchant', 'Merchant'),
        ('education', 'Educational/Service Provider'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='providers', null=True, blank=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    languages_spoken = models.CharField(max_length=200, blank=True)  # comma-separated e.g. "ja,vi,en"
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProviderVerification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='verifications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    certification_reference = models.CharField(max_length=100, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)


class Review(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # 1-5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('provider', 'author')