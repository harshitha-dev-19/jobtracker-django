from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from .forms import JobForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        password = request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('job_list')

    return render(request, 'myapp/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('job_list')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'myapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def job_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    query = request.GET.get('q')
    status = request.GET.get('status')

    jobs = Job.objects.filter(user=request.user)

    if query:
        jobs = jobs.filter(company__icontains=query)

    if status:
        jobs = jobs.filter(status__iexact=status)

    total = jobs.count()
    applied = jobs.filter(status="Applied").count()
    interview = jobs.filter(status="Interview").count()
    rejected = jobs.filter(status="Rejected").count()
    offer = jobs.filter(status="Offer").count()

    context = {
        'jobs': jobs,
        'total': total,
        'applied': applied,
        'interview': interview,
        'rejected': rejected,
        'offer': offer
    }

    return render(request, 'myapp/job_list.html', context)


def add_job(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()

    return render(request, 'myapp/job_form.html', {'form': form})


def update_job(request, id):
    job = get_object_or_404(Job, id=id, user=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm(instance=job)

    return render(request, 'myapp/job_form.html', {'form': form})


def delete_job(request, id):
    job = get_object_or_404(Job, id=id, user=request.user)
    job.delete()
    return redirect('job_list')