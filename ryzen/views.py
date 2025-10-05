from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Member
from .forms import OnboardForm

@login_required
def onboard_view(request):
    """Allow a logged-in user to join a stokvel and update their member info."""
    member, created = Member.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = OnboardForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            stokvel = form.cleaned_data["stokvel"]
            
            # Add the member to the stokvel's member list
            stokvel.members.add(member)
            member.stokvel = stokvel
            member.save()

            messages.success(request, f"You have successfully joined {stokvel.name}!")
            return redirect("stokvel_dashboard")  # change to your preferred page
    else:
        form = OnboardForm(instance=member)

    return render(request, "stokvel/onboard.html", {"form": form})

def dashboard_view(request):
    """Display the dashboard for the logged-in user."""
    if not request.user.is_authenticated:
        return redirect("login")

    member = Member.objects.filter(user=request.user).first()
    if not member or not member.stokvel:
        messages.info(request, "You are not part of any stokvel. Please join one.")
        return redirect("onboard")

    stokvel = member.stokvel
    contributions = FinancialRecord.objects.filter(member__stokvel=stokvel)
    total_balance = sum(c.amount for c in contributions)
    member_contribution = contributions.filter(member=member, month=date.today().month).first()

    # Example placeholders — you can connect to your Meeting model later
    next_meeting_date = date(2024, 12, 15)
    total_members = stokvel.member_set.count()
    active_members = stokvel.member_set.filter(is_active=True).count()

    # Example progress for a specific month
    target_amount = total_members * stokvel.contribution_amount
    current_month_total = sum(c.amount for c in contributions if c.date.month == date.today().month)
    progress_percentage = int((current_month_total / target_amount) * 100) if target_amount else 0
    remaining_amount = target_amount - current_month_total

    context = {
        "member": member,
        "stokvel": stokvel,
        "total_balance": total_balance,
        "member_contribution": member_contribution.amount if member_contribution else 0,
        "active_members": active_members,
        "total_members": total_members,
        "next_meeting_date": next_meeting_date,
        "progress_percentage": progress_percentage,
        "target_amount": target_amount,
        "remaining_amount": remaining_amount,
    }

    return render(request, "stokvel/dashboard.html", context)