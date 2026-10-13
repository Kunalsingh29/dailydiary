from django.shortcuts import render


def home(request):
    """Landing page. Will later redirect authed users to their calendar."""
    return render(request, "home.html")
