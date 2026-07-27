from django.shortcuts import render


def home(request):
    return render(request, "public_interface/home.html")
