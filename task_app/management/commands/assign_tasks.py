from django.core.management.base import BaseCommand
import time
from task_app.services import assign_pending_tasks

class Command(BaseCommand):
    help = "Automatic task distribution every 10 seconds"

    def handle(self, *args, **kwargs):
        self.stdout.write("Task dispatcher started. Press Ctrl+C to stop.")

        try:
            while True:
                assign_pending_tasks()
                time.sleep(10)
        except KeyboardInterrupt:
            self.stdout.write("Stopped.")