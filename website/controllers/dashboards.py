from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import *
from bloodster.locationMatching import find_matching_donors, find_matching_donors_for_all_requests, find_matching_requests


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from ..models import *
from bloodster.locationMatching import find_matching_donors, find_matching_donors_for_all_requests, find_matching_requests


@login_required
def donor_dashboard(request):
    if request.user.user_type != "donor":
        messages.error(request, "You're not allowed to visit donor Dashboard")
        return redirect('home')

    matching_requests = find_matching_requests(request.user)
    all_requests = BloodRequest.objects.filter(status='pending')
    accepted_requests = BloodRequest.objects.filter(
        fulfilled_by=request.user, status='in_progress')
    donations = BloodDonation.objects.filter(donor=request.user)

    # Calculate remaining days until the next donation
    remaining_days = None
    message = ""

    if request.user.last_donation:
        days_since_last_donation = (
            timezone.now() - request.user.last_donation).days
        if days_since_last_donation < 60:
            remaining_days = 60 - days_since_last_donation
            message = "You are eligible to donate blood in:"
        else:
            remaining_days = 0  # Eligible to donate immediately
            message = "You are eligible to donate blood now!"
    else:
        # If there is no last donation, indicate that they can donate
        message = "You are allowed to donate blood."

    context = {
        "matching_requests": matching_requests,
        "all_requests": all_requests,
        "accepted_requests": accepted_requests,
        "donations": donations,
        "remaining_days": remaining_days,
        "message": message,
    }
    return render(request, 'db/donor.html', context)


@login_required
def recipt_dashboard(request):

    if request.user.user_type != "recipient":
        messages.error(
            request, "You're not allowed to visit Recipient Dashboard")
        return redirect('home')

    blood_requests = BloodRequest.objects.filter(recipient=request.user)

    matching_donors = find_matching_donors_for_all_requests(request.user)

    all_donors = User.objects.filter(user_type='donor').exclude(
        id__in=[donor.id for donor in matching_donors])

    donations_to_confirm = BloodDonation.objects.filter(
        recipient=request.user, is_verified=False)

    context = {
        'requests': blood_requests,

        'matching_donors': matching_donors,
        'all_donors': all_donors,
        'donations_confirmation': donations_to_confirm
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
