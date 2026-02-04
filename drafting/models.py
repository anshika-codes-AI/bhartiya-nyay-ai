from django.db import models
from users.models import User

class DraftType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name



class Draft(models.Model):
    STATUS_CHOICES = [
        ("CREATED", "Created"),
        ("FACTS_COLLECTED", "Facts Collected"),
        ("LEGAL_MAPPED", "Legal Mapping Done"),
        ("DRAFT_GENERATED", "Draft Generated"),
        ("REVIEWED", "Reviewed"),
        ("EXPORTED", "Exported"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    draft_type = models.ForeignKey(DraftType, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="CREATED"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class DraftFact(models.Model):
    draft = models.ForeignKey(
        Draft, on_delete=models.CASCADE, related_name="facts"
    )
    key = models.CharField(max_length=100)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("draft", "key")

    def __str__(self):
        return f"{self.key}: {self.value}"