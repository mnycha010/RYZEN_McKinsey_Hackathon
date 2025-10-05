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
