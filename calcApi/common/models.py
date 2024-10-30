from django.contrib.auth.models import User
from django.db import models


class ApiRequest (models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    request = models.CharField(max_length=100)
    file = models.FileField(upload_to='files')


class ApiResponse (models.Model):
    request = models.ForeignKey(ApiRequest, related_name='responses', on_delete=models.CASCADE)
    response = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.request} - {self.response}"