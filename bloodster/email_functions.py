from django.core.mail import send_mail
from django.conf import settings


def send_request_email(recipient_email, donor_email, action, request_details):
    print("Sending Email...!")
    subject = f'Blood Request Update: {action.capitalize()}'
    message = f"""
    Dear User,

    The following blood request has been {action}:

    Blood Group: {request_details['blood_group']}
    Urgency: {request_details['urgency']}
    Location: {request_details['location']}
    Additional Info: {request_details['additional_info']}

    Please contact your respective donor or recipient for further information.

    Regards,
    BloodSter Team
    """

    recipient_list = [recipient_email, donor_email]

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )


def send_verification_email(email, verification_uuid):
    subject = 'Verify Your Account'
    verification_link = f'http://localhost:8000/verify/{verification_uuid}/'
    message = f"""
    Dear User,

    Please click the link below to verify your account:
    {verification_link}

    If you did not sign up for this account, please ignore this email.

    Regards,
    BloodSter Team
    """
    print('*'*20)
    print(verification_link)
    print('*'*20)

    recipient_list = [email]

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )
