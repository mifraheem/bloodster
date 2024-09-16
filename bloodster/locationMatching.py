from difflib import SequenceMatcher
from django.utils import timezone
from datetime import timedelta
from website.models import User, BloodRequest, BloodDonation


def location_similarity(loc1, loc2):
    """
    A function to calculate the similarity between two locations.
    Using SequenceMatcher from difflib for a basic similarity check.
    Returns a similarity ratio (0 to 1).
    """
    return SequenceMatcher(None, loc1.lower(), loc2.lower()).ratio()


def find_matching_donors(blood_request):
    """
    Find matching donors based on the recipient's blood request and location.
    """
    print(blood_request.requested_blood_group)
    potential_donors = User.objects.filter(
        user_type='donor',
        blood_group=blood_request.requested_blood_group
    )
    print(potential_donors)

    matching_donors = []

    for donor in potential_donors:
        similarity_ratio = location_similarity(
            blood_request.location, donor.location)
        print(similarity_ratio)

        if similarity_ratio >= 0.3:
            matching_donors.append((donor, similarity_ratio))

    # Sort donors by similarity score (highest first)
    matching_donors.sort(key=lambda x: x[1], reverse=True)

    # Return only donors, ignore similarity ratio for output
    return [donor[0] for donor in matching_donors]


def find_matching_requests(donor):
    """
    Find matching blood requests based on the donor's location.
    """
    # Get all blood requests
    all_requests = BloodRequest.objects.filter(status='pending')

    # List to store matching requests
    matching_requests = []

    for request in all_requests:
        # Check if the donor's blood group matches the request's required blood group
        if donor.blood_group == request.requested_blood_group:
            # Check the location similarity
            similarity_ratio = location_similarity(
                request.location, donor.location)

            # You can adjust the threshold for matching location similarity (e.g., 0.5 means 50% similarity)
            if similarity_ratio >= 0.5:
                matching_requests.append((request, similarity_ratio))

    # Sort requests by similarity score (highest first)
    matching_requests.sort(key=lambda x: x[1], reverse=True)

    # Return only requests, ignore similarity ratio for output
    return [request[0] for request in matching_requests]


def find_matching_donors_for_all_requests(recipient):
    """
    Find matching donors for all blood requests of a specific recipient
    and return only those with a location similarity ratio >= 0.3.
    """
    # Get all blood requests for the recipient
    recipient_requests = BloodRequest.objects.filter(
        recipient=recipient, status='pending')

    # Set to store unique matching donors
    matching_donors = set()

    for request in recipient_requests:
        print(
            f"Processing request for {request.requested_blood_group} at {request.location}")

        potential_donors = User.objects.filter(
            user_type='donor',
            blood_group=request.requested_blood_group
        )
        print("Potential donors:", potential_donors)

        for donor in potential_donors:
            similarity_ratio = location_similarity(
                request.location, donor.location)
            print(f"Donor: {donor}, Similarity Ratio: {similarity_ratio}")

            if similarity_ratio >= 0.3:
                # Add donor to the set if ratio >= 0.3
                matching_donors.add(donor)

    # Return the list of unique donors who matched the criteria
    return list(matching_donors)
