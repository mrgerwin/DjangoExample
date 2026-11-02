import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

import csv
from blog.models import Teacher

with open("Teacher.csv", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        Teacher.objects.update_or_create(
            id=int(row["id"]),
            defaults={
                "lastName": row["lastName"]
            }
        )

print("Teachers imported.")