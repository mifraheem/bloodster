import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@csrf_exempt
def donor_chatbot(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)
    user_message = data.get("message", "")

    if not user_message:
        return JsonResponse({"reply": "Please ask a question."})

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Bloodster Donor Assistant",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful blood donation assistant for donors. Answer clearly and safely."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "max_tokens": 200
            },
            timeout=20
        )

        result = response.json()
        reply = result["choices"][0]["message"]["content"]

        return JsonResponse({"reply": reply})

    except Exception as e:
        print("OPENROUTER ERROR:", e)
        return JsonResponse(
            {"reply": "AI service is temporarily unavailable."},
            status=500
        )

@login_required
def donor_chatbot_page(request):
    return render(request, "web/donor_chatbot.html", {
        "title": "Donor Assistant"
    })
