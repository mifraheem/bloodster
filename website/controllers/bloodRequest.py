from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from ..models import BloodRequest, BloodDonation


@login_required
def create_blood_request(request):
    if request.method == 'POST':
        requested_blood_group = request.POST.get('requested_blood_group')
        urgency = request.POST.get('urgency')
        location = request.POST.get('location')
        additional_info = request.POST.get('additional_info')

        # Create the BloodRequest instance
        BloodRequest.objects.create(
            recipient=request.user,
            requested_blood_group=requested_blood_group,
            urgency=urgency,
            location=location,
            additional_info=additional_info
        )
        print('i got your request')
        messages.success(request, "Your Request has been Saved.")
        return redirect('recipient-dashboard')
    else:
        messages.warning(request, "Bad request")


@login_required
def cancel_request(request, id):
    target_request = BloodRequest.objects.filter(id=id).first()
    if not target_request:
        messages.error(request, "Invalid Request Reference")
        return redirect('home')

    if target_request.status == 'fulfilled':
        messages.error(request, "Fulfilled Requests Can't be Cancel")
        return redirect('recipient-dashboard')

    target_request.status = 'cancelled'
    target_request.save()
    messages.info(request, "Your Blood Request has been cancelled")
    return redirect('recipient-dashboard')


@login_required
def view_request(request, id):
    target_request = BloodRequest.objects.filter(id=id).first()
    if not target_request:
        messages.info(request, "Invalid Request")
        return redirect('recipient-dashboard')

    context = {
        'blood_request': target_request
    }
    return render(request, 'web/request.html', context)


@login_required
def accept_blood_request(request, request_id):
    if request.user.user_type != "donor":
        messages.error(
            request, "You're not authorized to accept blood requests.")
        return redirect('home')

    # Get the blood request object
    blood_request = get_object_or_404(BloodRequest, id=request_id)

    # Ensure the request is still pending or available
    if blood_request.status != 'pending':
        messages.error(request, "This blood request is no longer available.")
        return redirect('donor-dashboard')

    # Assign the donor to the fulfilled_by field and update the status
    blood_request.fulfilled_by = request.user
    blood_request.status = 'in_progress'
    blood_request.save()

    messages.success(
        request, "You have successfully accepted the blood request.")
    return redirect('donor-dashboard')


@login_required
def fulfill_request(request, request_id):
    target_request = get_object_or_404(BloodRequest, id=request_id)

    # Check if user is the correct donor
    if request.user.user_type != 'donor' or request.user != target_request.fulfilled_by:
        messages.error(request, "You're not allowed to fulfill this request.")
        return redirect('home')

    # Ensure the request is still available for fulfillment
    if target_request.status != 'in_progress':
        messages.warning(request, "This request is not available to fulfill.")
        return redirect('home')

    target_request.status = 'fulfilled'
    target_request.save()

    BloodDonation.objects.create(
        donor=request.user,
        recipient=target_request.recipient,
        location=target_request.location,
        blood_request=target_request
    )

    messages.success(
        request, "Blood request marked as fulfilled and donation recorded.")
    return redirect('donor-dashboard')


@login_required
def confirm_donation_by_recipient(request, id):
    target_donation = get_object_or_404(
        BloodDonation, id=id, recipient=request.user)

    # Check if the donation is already verified
    if target_donation.is_verified:
        messages.error(request, "This donation is already verified.")
        return redirect('recipient-dashboard')

    target_donation.is_verified = True
    target_donation.save()

    # Confirmation message
    messages.success(request, "Thank you for your confirmation.")
    return redirect('recipient-dashboard')


@login_required
def reject_donation_by_recipient(request, id):
    target_donation = get_object_or_404(
        BloodDonation, id=id, recipient=request.user)

    if target_donation.blood_request:
        target_donation.blood_request.status = 'pending'
        target_donation.donor = None
        target_donation.blood_request.save()

    target_donation.delete()

    messages.success(request, "This donation has been rejected and deleted.")

    return redirect('recipient-dashboard')
