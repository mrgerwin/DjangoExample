# upload_students.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

import csv
from blog.models import Student


with open("Student.csv", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        Student.objects.update_or_create(
            id=int(row["id"]),
            defaults={
                "firstName": row["firstName"],
                "lastName": row["lastName"],
                "shTeacher_id": int(row["shTeacher_id"]),
                "successTeacher_id": int(row["successTeacher_id"]),
            }
        )

print("Students imported.")