from django.shortcuts import render, get_object_or_404
from .models import Post, HallPassRequest
from django.utils import timezone
from .forms import PostForm, HallPassForm
from django.shortcuts import redirect

# Create your views here.


def HallPass(request):
    print(request)
    if request.method == "POST":
        form = HallPassForm(request.POST)
        if form.is_valid():
            hallpass = form.save(commit=False)
            
            tempDate = form.cleaned_data.get('pass_date')
            tempPeriod = form.cleaned_data.get('period')
            tempStudent = form.cleaned_data.get('student')
            tempDestination = form.cleaned_data.get('destination')
            tempSendingTeacher = form.cleaned_data.get('sending_teacher')
            tempReceivingTeacher = form.cleaned_data.get('receiving_teacher')
            
            hallpass.period = tempPeriod
            hallpass.pass_date = tempDate
            hallpass.student = tempStudent
            hallpass.destination = tempDestination
            hallpass.sending_teacher = tempSendingTeacher
            hallpass.receiving_teacher = tempReceivingTeacher
            hallpass.timestamp = timezone.now()
            hallpass.status = "PENDING"
            hallpass.is_notified = False
            hallpass.save()
            return render(request, 'partials/teacher_dashboard.html', {})
        else:
            print("form errors:", form.errors)
    else:
        form = HallPassForm()
    return render(request, 'partials/student_pass.html', {'form':form})

def teacher_dashboard(request):
    return render(request, 'partials/teacher_dashboard.html', {})

def check_teacher_notifications(request):
    #print("checked server")
    if not request.user.is_authenticated:
        return render(request, 'partials/empty.html', {})
    new_requests = HallPassRequest.objects.filter(
        teacher = request.user,
        status = 'PENDING',
        is_notified = False
        )
    if new_requests.exists():
        return render(request, 'partials/notification_alert.html', { 'requests': new_requests})
    
    return render(request, 'partials/empty.html',{})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def error(request):
    return render(request, 'partials/error.html', {'hallpass': hallpass})
    