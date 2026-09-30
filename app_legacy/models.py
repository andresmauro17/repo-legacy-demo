"""Models for the Legacy application."""

from django.db import models


class LegacyModel(models.Model):
    """
    Core legacy model, originally introduced in 2015.
    Consumed as a shared Oracle-backed entity by three downstream
    applications: reporting-service, sync-service, and auth-gateway.
    """

    name = models.CharField(max_length=255)
    legacy_code = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def legacy_code_upper(self) -> str:
        """
        Legacy business logic consumed directly by three downstream
        repositories. Any signature or behavior change here has a
        known blast radius — see ARCHITECTURE.md.
        """
        return self.legacy_code.upper()