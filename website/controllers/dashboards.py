from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import *
from bloodster.locationMatching import find_matching_donors, find_matching_donors_for_all_requests, find_matching_requests


@login_required
def donor_dashboard(request):
    if request.user.user_type != "donor":
        messages.error(
            request, "You're not allowed to visit donor Dashboard")
        return redirect('home')
    matching_requests = find_matching_requests(request.user)
    context = {
        "matching_requests": matching_requests
    }
    return render(request, 'db/donor.html', context)


@login_required
def recipt_dashboard(request):

    if request.user.user_type != "recipient":
        messages.error(
            request, "You're not allowed to visit Recipient Dashboard")
        return redirect('home')

    # Get all blood requests for the logged-in recipient
    blood_requests = BloodRequest.objects.filter(recipient=request.user)

    matching_donors = find_matching_donors_for_all_requests(request.user)

    # Get all donors excluding the matched ones
    all_donors = User.objects.filter(user_type='donor').exclude(
        id__in=[donor.id for donor in matching_donors])

    context = {
        'requests': blood_requests,

        'matching_donors': matching_donors,
        'all_donors': all_donors  # Donors not matched based on location
    }

    return render(request, 'db/recipient.html', context)


@login_required
def show_donor_profile(request, id):
    donor = User.objects.filter(id=id, user_type='donor').first()
    if not donor:
        messages.error(request, "Invalid Donor")
    context = {
        'donor': donor
    }
    return render(request, 'db/donorProfile.html', context)
