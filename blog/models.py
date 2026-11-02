from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Teacher(models.Model):
    lastName = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.lastName

class Student(models.Model):
    firstName = models.CharField(max_length = 100)
    lastName = models.CharField(max_length = 100)
    successTeacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='success_students'
    )
    shTeacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sh_students'
    )
    
    def __str__(self):
        return (self.firstName + " " + self.lastName)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
class HallPassRequest(models.Model):
    
    PERIOD_CHOICES = [("SUCCESS", "Success"), ("STUDYHALL", "Study Hall"),]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    #TO DO make the foreign key make sense
    #sending_teacher = models.ForeignKey(User, on_delete = models.CASCADE, related_name="teacher_requests")
    sending_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="sent_hallpass_requests")
    receiving_teacher =models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="received_hallpass_requests")
    
    destination = models.CharField(max_length = 100)
    
    pass_date = models.DateField(default=timezone.localdate)
    
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default="SUCCESS")
    
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length = 20,
        choices = [('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('DENIED', 'Denied')], default='PENDING'
        )
    is_notified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student} -> from {self.sending_teacher} to {self.receiving_teacher} with destination {self.destination} ({self.status})"