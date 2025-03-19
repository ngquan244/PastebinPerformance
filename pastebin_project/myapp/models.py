from django.db import models
import uuid
from django.utils import timezone

class Paste(models.Model):
    title = models.CharField(max_length=255, default="Untitled")  # Thêm tiêu đề
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def has_expired(self):
        return self.expires_at and timezone.now() > self.expires_at

class Analytics(models.Model):
    paste = models.OneToOneField(Paste, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
