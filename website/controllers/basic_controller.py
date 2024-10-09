from django.shortcuts import render, redirect, HttpResponse
from website.models import *
from django.contrib import messages


def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, 'web/campaigns.html', {'campaigns': campaigns})


def full_gallery(request):
    all_images = Gallery.objects.all()
    return render(request, 'gallery.html', {'all_images': all_images})


def home(request):
    latest_campaigns = Campaign.objects.order_by('-date')[:4]
    gallery_images = Gallery.objects.all()[:10]
    return render(request, 'index.html', {
        'latest_campaigns': latest_campaigns,
        'gallery_images': gallery_images
    })


def contect_message(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        message = data.get('message')
        QuickMessage.objects.create(
            name=name, mobile_no=phone, email=email, message=message)
        messages.success(request, "Your Message has been Saved.")
    return redirect('home')
