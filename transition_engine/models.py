from django.db import models

# Create your models here.



class LegalSection(models.Model):
    act = models.CharField(max_length=20)  # IPC / BNS / BNSS
    section_number = models.CharField(max_length=20)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.act} {self.section_number}"


class SectionMapping(models.Model):
    ipc_section = models.ForeignKey(
        LegalSection,
        on_delete=models.CASCADE,
        related_name="ipc_mappings"
    )
    bns_section = models.ForeignKey(
        LegalSection,
        on_delete=models.CASCADE,
        related_name="bns_mappings"
    )
    intent = models.CharField(max_length=255)
    drafting_note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.ipc_section} → {self.bns_section}"