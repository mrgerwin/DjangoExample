from django import forms

from .models import Post, HallPassRequest, Student, Teacher

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ("title", "text")
        
class HallPassForm(forms.ModelForm):
    class Meta:
        model = HallPassRequest
        
        fields = ['pass_date', 'period', 'student','sending_teacher', 'receiving_teacher', 'destination', 'status']
        
        widgets = {'pass_date': forms.DateInput(attrs={'type':'date'}),}