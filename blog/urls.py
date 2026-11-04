from django.urls import path
from . import views

urlpatterns = [
    path('',views.teacher_dashboard, name='teacher_dashboard'),
    path('check_notifications', views.check_teacher_notifications, name='check_notifications'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('new_pass', views.HallPass, name='new_pass'),
    path('partials/error.html', views.error , name='error'),
    path('update_status/<int:pass_id>/',views.update_status,name='update_status'),
    ]
