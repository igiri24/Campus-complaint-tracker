from django.conf import settings
from django.db import models

class Complaint(models.Model):
    class Category(models.TextChoices):
        MAINTENANCE = "maintenance", "Maintenance"
        CLEANLINESS = "cleanliness", "Cleanliness"
        IT = "it", "IT & Wi-Fi"
        ACADEMIC = "academic", "Academic"
        SAFETY = "safety", "Safety"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        REVIEW = "review", "In review"
        PROGRESS = "progress", "In progress"
        RESOLVED = "resolved", "Resolved"
        REJECTED = "rejected", "Rejected"

    title = models.CharField(max_length=140)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices)
    location = models.CharField(max_length=140)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="complaints")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_complaints")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"CT-{self.pk:04d} · {self.title}"

class ComplaintUpdate(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="updates")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=Complaint.Status.choices)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Update for {self.complaint}"
