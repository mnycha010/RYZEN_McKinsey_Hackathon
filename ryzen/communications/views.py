from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from member.models import Member
from .models import CoordinatorMessage, Notification
from .forms import CoordinatorMessageForm


def coordinators_view(request):
    if not request.user.is_authenticated:
        return redirect("core:login")

    member = Member.objects.filter(user=request.user).first()
    if not member or not member.stokvel:
        messages.info(request, "You are not part of any stokvel.")
        return redirect("onboard")

    stokvel = member.stokvel

    # ----------------------------
    # Handle form submission
    # ----------------------------
    if request.method == "POST":
        form = CoordinatorMessageForm(request.POST)
        selected_members = request.POST.getlist("target_members")  # IDs of selected members
        if form.is_valid():
            msg = form.save(commit=False)
            msg.stokvel = stokvel
            msg.sender = request.user
            msg.save()
            form.save_m2m()

            category = form.cleaned_data.get("category") or "general"

            targets = msg.target_members.all() if msg.target_members.exists() else stokvel.members.all()
            for m in targets:
                Notification.objects.create(
                    user=m.user,
                    title=f"Communication : {msg.sender.get_full_name() or msg.sender.username}",
                    message=msg.message,
                    category=category
                )
            messages.success(request, "Message sent successfully!")
            return redirect("communications:coordinators")
    else:
        form = CoordinatorMessageForm()
        selected_members = []

    form.fields['target_members'].queryset = stokvel.members.all()

    # ----------------------------
    # Paginate messages
    # ----------------------------
    messages_qs = CoordinatorMessage.objects.filter(stokvel=stokvel).order_by('-created_at')
    paginator = Paginator(messages_qs, 10)
    page_number = request.GET.get('page')
    messages_page = paginator.get_page(page_number)

    context = {
        "member": member,
        "stokvel": stokvel,
        "form": form,
        "messages_page": messages_page,
        "selected_members": selected_members,
    }
    return render(request, "communications/coordinators.html", context)



def notifications_view(request):
    if not request.user.is_authenticated:
        return redirect("core:login")

    notifications_qs = request.user.notifications.order_by('-created_at')
    paginator = Paginator(notifications_qs, 10)
    page_number = request.GET.get('page')
    notifications_page = paginator.get_page(page_number)

    context = {
        "notifications_page": notifications_page
    }
    return render(request, "communications/notifications.html", context)
