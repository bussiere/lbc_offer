from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate


from django.contrib.auth.models import User
import json


from .models import Token

# Create your views here.
@csrf_exempt
def TokenAuth(request):
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        user = authenticate(
            username=received_json_data["Username"],
            password=received_json_data["Password"],
        )
        if not user:
            try:
                username = received_json_data["Username"]
                user = User.objects.get(email=username)
                user = authenticate(
                    username=user.username, password=received_json_data["Password"]
                )
            except Exception as e:
                print(e)
                return JsonResponse({"Error": "Invalid log password ", "Status": "Ko"})
        if user and user.is_active:
            token = Token(user=user)
            token.save()
            return JsonResponse({"Token": token.value, "Status": "Ok"})
        return JsonResponse(
            {
                "Error": """
                Bad Auth
                Bad Auth
                Bad Auth
                
                He rides across the nation
                The thoroughbred of sin
                He got the application
                That you just sent in
                
                It needs evaluation
                So let the games begin""",
                "Status": "Ko",
            }
        )
