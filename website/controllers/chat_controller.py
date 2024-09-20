from django.utils.dateparse import parse_datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import User, Message
from django.contrib import messages
from django.db.models import Q


@login_required
def chat(request, chat_user=None):
    chat = False
    target_user = None
    chats = None

    if chat_user:
        chat = True
        target_user = get_object_or_404(User, username=chat_user)
        print(f'You are trying to get chat with {chat_user}')

        chats = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=target_user)) |
            (Q(sender=target_user) & Q(receiver=request.user))
        ).order_by('timestamp')

    all_users = User.objects.exclude(
        (Q(id=request.user.id)) | (Q(is_superuser=True))
    )

    context = {
        'all_users': all_users,
        'chats': chats,
        'chat_user': target_user,
    }

    return render(request, 'web/chat.html', context)


@csrf_exempt
def save_message(request, chat_user):
    if request.method == 'POST':

        target_user = get_object_or_404(User, username=chat_user)

        message = request.POST.get('message')

        if message and message.strip():

            new_message = Message.objects.create(
                receiver=target_user,
                sender=request.user,
                content=message
            )

            return JsonResponse({
                'success': True,
                'chat': {
                    'sender': new_message.sender.username,
                    'content': new_message.content,
                    'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                }
            })

        return JsonResponse({'success': False, 'error': 'Message cannot be empty'}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


def fetch_all_messages(request, chat_user):
    if request.method == 'GET':

        target_user = get_object_or_404(User, username=chat_user)

        all_messages = Message.objects.filter(
            receiver=request.user, sender=target_user
        ) | Message.objects.filter(
            receiver=target_user, sender=request.user
        )
        all_messages = all_messages.order_by('timestamp')

        # Prepare messages for JSON response
        messages_list = []
        for message in all_messages:
            messages_list.append({
                'sender': message.sender.username,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                # Check if the current user is the sender
                'is_sender': message.sender == request.user
            })

        return JsonResponse({'success': True, 'messages': messages_list})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
