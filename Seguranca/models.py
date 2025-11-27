from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class PasswordResetRequest(models.Model):
    """
    Model to store temporary password reset requests. 
    Each request is linked to a user and contains a hashed temporary password.
    The temporary password is deleted after use or after a certain period of time (15 minutes).
    """

    EXPIRATION_TIME_MINUTES = 15

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    temporary_password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_temporary_password(self, raw_password):
        self.temporary_password_hash = make_password(raw_password)

    def is_expired(self):
        """Checks if the password reset request has expired."""
        expiration_delta = timezone.timedelta(minutes=self.EXPIRATION_TIME_MINUTES)
        return timezone.now() > self.created_at + expiration_delta

    def check_temporary_password(self, raw_password):
        """
        Checks if the provided raw password is correct and the request has not expired.
        """
        if self.is_expired():
            return False
        return check_password(raw_password, self.temporary_password_hash)