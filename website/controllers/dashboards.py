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
    all_requests = BloodRequest.objects.filter(status='pending')
    accepted_requests = BloodRequest.objects.filter(
        fulfilled_by=request.user, status='in_progress')
    donations = BloodDonation.objects.filter(
        donor=request.user)

    context = {
        "matching_requests": matching_requests,
        "all_requests": all_requests,
        "accepted_requests": accepted_requests,
        "donations": donations
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
