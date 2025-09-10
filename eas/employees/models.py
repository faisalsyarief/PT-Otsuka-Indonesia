from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, nama, password=None, **extra_fields):
        if not email:
            raise ValueError("Email wajib")
        email = self.normalize_email(email)
        username = extra_fields.pop("username", None) or email

        user = self.model(email=email, nama=nama, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nama, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, nama, password, **extra_fields)


class CustomUser(AbstractUser):
    nama = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    jabatan = models.CharField(max_length=150, blank=True, null=True)
    tanggal_masuk = models.DateField(blank=True, null=True)
    status_aktif = models.BooleanField(default=True)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "nama"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.nama} ({self.email})"