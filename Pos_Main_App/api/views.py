from rest_framework.views import APIView
from Pos_Main_App.models import Dishes_model, Bill_model, OrderedDish_model, Employe_model,Table_model,ContactSupport
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from Pos_Main_App.api.serializers  import Dishes_Serializer, Employe_Serializer, Bill_Serializer, OrderedDish_Serializer, Table_Serializer,ContactSupportSerializer
from Pos_Main_App.api.filters import Dishes_filter, OrderedDish_filter,Bill_filter, Employe_filter, Table_filter
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import send_slack_error_message
import requests
from rest_framework import status
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
import traceback
from .utils import send_slack_notification 

def health_check(request):
    return JsonResponse({"status": "OK"})

def api_data(request):
    if request.method == 'GET':
        data = {
            "message": "Hello from the backend!",
            "status": "success"
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


class Dishes_View(generics.ListCreateAPIView):
    queryset = Dishes_model.objects.all()
    serializer_class= Dishes_Serializer
    filter_backends= [DjangoFilterBackend]
    filterset_class= Dishes_filter



class Dishes_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset= Dishes_model.objects.all()
    serializer_class= Dishes_Serializer







class Bill_View(generics.ListCreateAPIView):
    queryset = Bill_model.objects.all()
    serializer_class= Bill_Serializer
    filter_backends= [DjangoFilterBackend]
    filterset_class=Bill_filter



class Bill_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bill_model.objects.all()
    serializer_class = Bill_Serializer   






class OrderDishes_View(generics.ListCreateAPIView):
    queryset = OrderedDish_model.objects.all()
    serializer_class= OrderedDish_Serializer
    filter_backends= [DjangoFilterBackend]
    filterset_class= OrderedDish_filter



class orderDishes_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderedDish_model.objects.all()
    serializer_class = OrderedDish_Serializer  









class Employe_View(generics.ListCreateAPIView):
    queryset = Employe_model.objects.all()
    serializer_class= Employe_Serializer
    filter_backends= [DjangoFilterBackend]
    filterset_class= Employe_filter


class Employe_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employe_model.objects.all()
    serializer_class = Employe_Serializer




class Table_View(generics.ListCreateAPIView):
    queryset = Table_model.objects.all()
    serializer_class= Table_Serializer
    filter_backends= [DjangoFilterBackend]
    filterset_class= Table_filter









import logging
from django.http import JsonResponse
from django.conf import settings
import traceback
logger = logging.getLogger(__name__)

SLACK_WEBHOOK_URL = settings.SLACK_WEBHOOK_URL  # Ensure this is set in settings.py

# def send_slack_error_message(error_message):
#     """Send error messages to Slack channel."""
#     if SLACK_WEBHOOK_URL:
#         payload = {"text": f":warning: ERROR: {error_message}"}
#         requests.post(SLACK_WEBHOOK_URL, json=payload)

# def test_slack_error(request):
#     """View to trigger an error and send a Slack message."""
#     try:
#         1 / 0  # This will cause a ZeroDivisionError
#     except Exception as e:
#         error_message = str(e)
#         logger.error(error_message)
#         send_slack_error_message(error_message)
#         return JsonResponse({"error": "An error occurred. Check Slack."}, status=500)




# def send_slack_error_message(error_message):
#     """Send error logs to Slack via Webhook."""
#     try:
#         payload = {"text": f"🚨 *ERROR ALERT* 🚨\n```{error_message}```"}
#         response = requests.post(SLACK_WEBHOOK_URL, json=payload)
#         if response.status_code != 200:
#             logger.error(f"Failed to send Slack message: {response.text}")
#     except Exception as e:
#         logger.error(f"Slack notification failed: {str(e)}")

# def test_slack_error(request):
#     """View to trigger an error and send a Slack message."""
#     try:
#         1 / 0  # Intentional ZeroDivisionError
#     except Exception as e:
#         error_message = traceback.format_exc()  # Get full error traceback
#         logger.error(error_message)
#         send_slack_error_message(error_message)
#         return JsonResponse({"error": "An error occurred. Check Slack."}, status=500)
    
    
from django.http import JsonResponse
import traceback
from .utils import send_slack_error_message

def test_slack_error(request):
    """View to trigger an error and send a Slack message."""
    try:
        1 / 0  # Intentional ZeroDivisionError
    except Exception as e:
        error_message = traceback.format_exc()  # Get full error traceback
        send_slack_error_message(error_message)  # Send to Slack
        return JsonResponse({"error": "An error occurred. Check Slack."}, status=500)




@method_decorator(csrf_exempt, name='dispatch')
class ContactSupportView(APIView):
    def get(self, request, *args, **kwargs):
        """Retrieve all contact support messages."""
        contacts = ContactSupport.objects.all()
        serializer = ContactSupportSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Submit a contact support request."""
        try:
            serializer = ContactSupportSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Contact request submitted successfully!"},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            error_message = traceback.format_exc()  # Capture full error traceback
            send_slack_notification(error_message, request)  # Send error to Slack
            return Response(
                {"error": "An internal server error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    