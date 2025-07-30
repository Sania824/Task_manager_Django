from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE


# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']
