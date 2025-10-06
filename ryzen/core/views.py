from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm

def home_view(request):
    """
    Homepage view
    """
    return render(request, "core/home.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("member:dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "core/login.html", {"form": form})


def logout_view(request):
    """
    Logs out the user
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("core:home")
