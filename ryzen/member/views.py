from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from stokvel.models import Stokvel
from .models import Member, FinancialRecord
from .forms import OnboardForm

def onboard_view(request):
    """
    Registration / Onboarding view:
    - Creates a User
    - Creates a Member profile
    - Links to a Stokvel by ID
    - Creates an initial FinancialRecord
    """
    if request.method == "POST":
        form = OnboardForm(request.POST)
        if form.is_valid():
            # Create user
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create member profile
            member = form.save(commit=False)
            member.user = user

            # Link stokvel by alphanumeric ID
            stokvel_id = form.cleaned_data["stokvel_id"]
            try:
                stokvel = Stokvel.objects.get(id=stokvel_id, active=True)
            except Stokvel.DoesNotExist:
                messages.error(request, "Stokvel ID not found or inactive.")
                user.delete()  # clean up created user
                return redirect("member:onboard")

            member.stokvel = stokvel
            member.save()

            # Add member to stokvel's member list
            stokvel.members.add(member)

            # Create initial financial record
            FinancialRecord.objects.create(member=member, amount_saved=0.0, amount_borrowed=0.0)

            messages.success(request, f"Account created! You have joined {stokvel.name}. Please login.")
            return redirect("login")
    else:
        form = OnboardForm()

    return render(request, "member/onboard.html", {"form": form})
