from django.shortcuts import render, redirect, HttpResponse
from website.models import *

def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, 'web/campaigns.html', {'campaigns': campaigns})

def full_gallery(request):
    all_images = Gallery.objects.all()  
    return render(request, 'gallery.html', {'all_images': all_images})

def home(request):
    latest_campaigns = Campaign.objects.order_by('-date')[:4]
    gallery_images = Gallery.objects.all()[:10]  # Fetch the first 10 images
    return render(request, 'index.html', {
        'latest_campaigns': latest_campaigns,
        'gallery_images': gallery_images  # Pass the gallery images to the template
    })


