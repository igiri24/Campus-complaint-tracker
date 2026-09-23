from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ComplaintForm, UpdateForm
from .models import Complaint, ComplaintUpdate


def home(request):
    return render(request, "complaints/home.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account is ready. You can now submit a complaint.")
        return redirect("dashboard")
    return render(request, "complaints/register.html", {"form": form})

@login_required
def dashboard(request):
    complaints = Complaint.objects.select_related("created_by", "assigned_to")
    if not request.user.is_staff:
        complaints = complaints.filter(Q(created_by=request.user) | Q(assigned_to=request.user))
    status = request.GET.get("status", "")
    category = request.GET.get("category", "")
    search = request.GET.get("q", "").strip()
    if status:
        complaints = complaints.filter(status=status)
    if category:
        complaints = complaints.filter(category=category)
    if search:
        complaints = complaints.filter(Q(title__icontains=search) | Q(location__icontains=search) | Q(description__icontains=search))
    mine = Complaint.objects.filter(created_by=request.user)
    context = {
        "complaints": complaints,
        "mine_count": mine.count(),
        "open_count": mine.exclude(status__in=[Complaint.Status.RESOLVED, Complaint.Status.REJECTED]).count(),
        "resolved_count": mine.filter(status=Complaint.Status.RESOLVED).count(),
        "status_choices": Complaint.Status.choices,
        "category_choices": Complaint.Category.choices,
        "selected_status": status,
        "selected_category": category,
        "query": search,
    }
    return render(request, "complaints/dashboard.html", context)

@login_required
def create_complaint(request):
    form = ComplaintForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        complaint = form.save(commit=False)
        complaint.created_by = request.user
        complaint.save()
        ComplaintUpdate.objects.create(complaint=complaint, author=request.user, status=complaint.status, comment="Complaint submitted.")
        messages.success(request, f"Complaint CT-{complaint.pk:04d} submitted successfully.")
        return redirect("complaint_detail", pk=complaint.pk)
    return render(request, "complaints/create.html", {"form": form})

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint.objects.select_related("created_by", "assigned_to").prefetch_related("updates__author"), pk=pk)
    if not request.user.is_staff and complaint.created_by_id != request.user.id and complaint.assigned_to_id != request.user.id:
        return render(request, "complaints/forbidden.html", status=403)
    return render(request, "complaints/detail.html", {"complaint": complaint})

@login_required
@user_passes_test(lambda user: user.is_staff)
def update_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    form = UpdateForm(request.POST or None, initial={"status": complaint.status})
    if request.method == "POST" and form.is_valid():
        complaint.status = form.cleaned_data["status"]
        if complaint.assigned_to is None:
            complaint.assigned_to = request.user
        complaint.save()
        ComplaintUpdate.objects.create(complaint=complaint, author=request.user, status=complaint.status, comment=form.cleaned_data["comment"])
        messages.success(request, "Complaint progress updated.")
        return redirect("complaint_detail", pk=complaint.pk)
    return render(request, "complaints/update.html", {"form": form, "complaint": complaint})
