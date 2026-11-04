from django.shortcuts import render, get_object_or_404
from .models import Post, HallPassRequest, Teacher, Student
from django.utils import timezone
from .forms import PostForm, HallPassForm
from django.shortcuts import redirect
from django.urls import reverse


# Create your views here.

def update_status(request, pass_id):
    if request.method == "POST":
        hallpass = get_object_or_404(
            HallPassRequest,
            id=pass_id
        )

        hallpass.status = request.POST.get("status")
        hallpass.save()
        teacher = request.POST.get("teacher")
        period = request.POST.get("period")

        return redirect(
            f"{reverse('teacher_dashboard')}?teacher={teacher}&period={period}"
        )

    return redirect("teacher_dashboard")

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
            tempStatus = form.cleaned_data.get('status')
            
            hallpass.period = tempPeriod
            hallpass.pass_date = tempDate
            hallpass.student = tempStudent
            hallpass.destination = tempDestination
            hallpass.sending_teacher = tempSendingTeacher
            hallpass.receiving_teacher = tempReceivingTeacher
            hallpass.timestamp = timezone.now()
            hallpass.status = tempStatus
            hallpass.is_notified = False
            hallpass.save()
            
            return redirect('teacher_dashboard')
        else:
            print("form errors:", form.errors)
    else:
        
        initial_data = {
        'student': request.GET.get('student'),
        'sending_teacher': request.GET.get('teacher'),
        'period': request.GET.get('period'),
        }

    form = HallPassForm(initial=initial_data)
    return render(request, 'partials/student_pass.html', {'form':form})

def teacher_dashboard(request):
    teachers = Teacher.objects.all()

    selected_teacher = request.GET.get('teacher')
    selected_period = request.GET.get('period')
    selected_teacher_name = None
    students = []
    receiving_passes_p=[]
    receiving_passes_a=[]
    receiving_passes_o=[]
    receiving_passes_r=[]
    receiving_passes_RECEIVED=[]
    
    pending_passes = []
    approved_passes = []
    out_passes =[]
    returned_passes =[]

    if selected_teacher and selected_period:
        selected_teacher_name = Teacher.objects.get(id=selected_teacher)
        selected_teacher = int(selected_teacher)
        print(type(selected_teacher))
        if selected_period == "SUCCESS":
            students = Student.objects.filter(
                successTeacher_id=selected_teacher
            ).order_by('lastName', 'firstName')

        elif selected_period == "SH":
            students = Student.objects.filter(
                shTeacher_id=selected_teacher
            ).order_by('lastName', 'firstName')
        if selected_teacher:
            pending_passes = HallPassRequest.objects.filter(sending_teacher_id = selected_teacher, status='PENDING')
            approved_passes = HallPassRequest.objects.filter(sending_teacher_id = selected_teacher, status='APPROVED')
            out_passes = HallPassRequest.objects.filter(sending_teacher_id = selected_teacher, status='OUT')
            returned_passes = HallPassRequest.objects.filter(sending_teacher_id = selected_teacher, status='RETURNED')
            received_passes = HallPassRequest.objects.filter(sending_teacher_id = selected_teacher, status='RECEIVED')
            receiving_passes_p = HallPassRequest.objects.filter(receiving_teacher_id = selected_teacher, status='PENDING')
            receiving_passes_a = HallPassRequest.objects.filter(receiving_teacher_id = selected_teacher, status='APPROVED')
            receiving_passes_o = HallPassRequest.objects.filter(receiving_teacher_id = selected_teacher, status='OUT')
            receiving_passes_r = HallPassRequest.objects.filter(receiving_teacher_id = selected_teacher, status='RETURNED')
            receiving_passes_RECEIVED=HallPassRequest.objects.filter(receiving_teacher_id = selected_teacher, status='RECEIVED')


    context = {
        'teachers': teachers,
        'students': students,
        'selected_teacher': selected_teacher,
        'selected_period': selected_period,
        'selected_teacher_name': selected_teacher_name,
        'pending_passes': pending_passes,
        'approved_passes': approved_passes,
        'out_passes': out_passes,
        'returned_passes': returned_passes,
        'received_passes': received_passes,
        'receiving_passes_p': receiving_passes_p,
        'receiving_passes_a': receiving_passes_a,
        'receiving_passes_o': receiving_passes_o,
        'receiving_passes_r': receiving_passes_r,
        'receiving_passes_RECEIVED': receiving_passes_RECEIVED,
        
    }
    
    return render(request, 'partials/teacher_dashboard.html', context)

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
    