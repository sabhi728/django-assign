from django.db import models
import uuid

class FAQ(models.Model):
    id = models.TextField(primary_key=True,default=uuid.uuid4)
    question = models.TextField()
    answer = models.TextField()


