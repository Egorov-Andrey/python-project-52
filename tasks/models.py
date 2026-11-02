from django.contrib.auth.models import User
from django.db import models

from labels.models import Label
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authored_tasks',
        null=True,
        blank=True
    )
    
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
    )
    
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='executor_tasks'
    )

    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name='tasks',
        help_text='Можно выбрать несколько меток'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.status.name})"