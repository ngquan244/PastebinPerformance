from django.utils import timezone
from .models import Paste

def cleanup_expired_pastes():
    Paste.objects.filter(expires_at__lt=timezone.now()).delete()
