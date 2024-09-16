# views.py
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import BloodRequest


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
    if target_request:
        target_request.delete()
        messages.info(request, "Your Blood Request has been cancelled")
    else:
        messages.error(request, "Invalid Blood Request Reference")

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
