from django.shortcuts import render, redirect, HttpResponse


def home(request):
    return render(request, "web/index.html")


def about(request):
    return render(request, "web/about.html")


def contact(request):
    return render(request, "web/contact.html")
