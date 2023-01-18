from django.contrib.auth.models import User
from django.db import models


class Character(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Character Public Information
    alliance_id = models.PositiveIntegerField(null=True)
    birthday = models.DateTimeField(null=True)
    bloodline_id = models.PositiveIntegerField(null=True)
    corporation_id = models.PositiveIntegerField(null=True)
    description = models.TextField(max_length=8192, null=True)
    gender = models.CharField(max_length=16, null=True)
    race_id = models.PositiveIntegerField(null=True)
    security_status = models.FloatField(null=True)

    def update(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    token_type = models.CharField(max_length=128)
    access_token = models.CharField(max_length=5140)
    refresh_token = models.CharField(max_length=128)
    expires_at = models.PositiveIntegerField()

    def update(
        self,
        access_token: str = None,
        refresh_token: str = None,
        expires_at: int = None,
        **kwargs
    ):
        if access_token:
            self.access_token = access_token
        if refresh_token:
            self.refresh_token = refresh_token
        if expires_at:
            self.expires_at = expires_at
        self.save()

    def to_dict(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )
