from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from hangarinapp.models import Category, Priority, Task, Note, SubTask


class Command(BaseCommand):
    help = "Create initial fake data for Tasks, Notes, and SubTasks"

    def handle(self, *args, **kwargs):
        self.create_tasks(30)
        self.create_notes(20)
        self.create_subtasks(40)

    def create_tasks(self, count):
        fake = Faker()
        for _ in range(count):
            Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(
                    elements=["Pending", "In Progress", "Completed"]
                ),
                category=Category.objects.order_by("?").first(),
                priority=Priority.objects.order_by("?").first(),
            )
        self.stdout.write(self.style.SUCCESS("Tasks created successfully."))

    def create_notes(self, count):
        fake = Faker()
        for _ in range(count):
            Note.objects.create(
                task=Task.objects.order_by("?").first(),
                content=fake.paragraph(nb_sentences=2),
            )
        self.stdout.write(self.style.SUCCESS("Notes created successfully."))

    def create_subtasks(self, count):
        fake = Faker()
        for _ in range(count):
            SubTask.objects.create(
                parent_task=Task.objects.order_by("?").first(),
                title=fake.sentence(nb_words=4),
                status=fake.random_element(
                    elements=["Pending", "In Progress", "Completed"]
                ),
            )
        self.stdout.write(self.style.SUCCESS("SubTasks created successfully."))