from django.db import models


class Worker(models.Model):
    name = models.CharField(max_length=100, unique=True)
    max_tasks = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


task_status = (
    ("pending", "Pending"),
    ("in_progress", "In progress"),
    ("completed", "completed"),
)

class Task(models.Model):
    PRIORITY_CHOICES = [(i, str(i)) for i in range(1, 6)]

    description = models.TextField()
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES, default=3)
    status = models.CharField(
        max_length=20,
        choices=task_status,
        default="pending",
    )
    task_type = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    worker = models.ForeignKey(
        Worker,
        related_name="tasks",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.id}: {self.description[:30]}"