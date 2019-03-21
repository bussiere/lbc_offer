from django.db import models
from django.contrib.auth.models import User
import uuid
import random
from django.utils import timezone

# Create your models here.


class Token(models.Model):
    created = models.DateTimeField(null=True, blank=True, editable=False)
    modified = models.DateTimeField(null=True, blank=True)
    version = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    timeLimit = models.DateTimeField(null=True, blank=True)
    value = models.CharField(unique=True, max_length=200, null=True, blank=True)

    def __str__(self):
        return (
            self.user.username
            + ":"
            + str(self.created)
            + ":"
            + str(self.modified)
            + ":"
            + str(self.id)
        )

    def __unicode__(self):
        return (
            self.user.username
            + ":"
            + str(self.created)
            + ":"
            + str(self.modified)
            + ":"
            + str(self.id)
        )

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.value = str(uuid.uuid4().hex.upper()) + str(random.randint(0, 100))
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Token, self).save(*args, **kwargs)
