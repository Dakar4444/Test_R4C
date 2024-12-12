from django.db import models


class RobotModel(models.Model):
    model = models.CharField(max_length=2, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.model


class Robot(models.Model):
    serial = models.CharField(max_length=6, blank=False, null=False, unique=True)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)

    def save(self, *args, **kwargs):
        self.serial = f"{self.model}-{self.version}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.serial