from django.db import models

# Create your models here.
from django.db import models


class Judgment(models.Model):
    court = models.CharField(max_length=255)
    case_title = models.CharField(max_length=500)
    citation = models.CharField(max_length=255, unique=True)
    judgment_date = models.DateField()

    # context
    acts = models.JSONField()  # ["IPC", "BNS", "BNSS"]
    sections = models.JSONField()  # ["IPC 420", "BNS 318"]

    source_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.case_title} ({self.citation})"
    
class JudgmentChunk(models.Model):
    judgment = models.ForeignKey(
        Judgment,
        on_delete=models.CASCADE,
        related_name="chunks"
    )

    text = models.TextField()

    # legal metadata (CRITICAL)
    relevant_sections = models.JSONField()  # ["BNS 318"]
    legal_issue = models.CharField(max_length=255)

    # vector placeholder (later)
    embedding = models.BinaryField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chunk of {self.judgment.citation}"