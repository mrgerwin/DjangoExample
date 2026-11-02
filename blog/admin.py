from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Student, HallPassRequest, Teacher

admin.site.register(Post)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(HallPassRequest)
