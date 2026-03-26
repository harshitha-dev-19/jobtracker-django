from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    status = models.CharField(max_length=20)

    def _str_(self):
        return f"{self.company} - {self.role}"