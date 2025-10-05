from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home_view(request):
    """
    Homepage view
    """
    return render(request, "core/home.html")


def login_view(request):
    """
    Handles user login
    """
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("core:home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "core/login.html")


def logout_view(request):
    """
    Logs out the user
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("core:home")
