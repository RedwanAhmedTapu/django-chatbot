from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re

from .models import ChatMessage
from .serializers import ChatMessageSerializer
from django.shortcuts import render
import random


def index(request):
    return render(request, 'chatbot/index.html')


class ChatView(APIView):
    def get(self, request):
        messages = ChatMessage.objects.all().order_by('created_at')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_message = request.data.get('user_message')
        bot_response = self.generate_bot_response(user_message)

        chat_message = ChatMessage.objects.create(
            user_message=user_message,
            bot_response=bot_response
        )
        serializer = ChatMessageSerializer(chat_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def generate_bot_response(self, user_message):
        user_message = user_message.lower()

        # Define intents and responses
        intents = {
            "price": {
                "patterns": [r".*\bprice\b.*", r".*\bcost\b.*", r".*\bhow much\b.*"],
                "responses": [
                    "The price of this product is $50. Would you like to know about discounts?",
                    "It costs $50. Would you like to explore financing options?",
                    "The price is $50. Are you interested in a bulk purchase?"
                ]
            },
            "delivery": {
                "patterns": [r".*\bdelivery\b.*", r".*\bshipping\b.*", r".*\bwhen will it arrive\b.*"],
                "responses": [
                    "We offer free delivery on orders above $100. Would you like to know more?",
                    "Standard shipping takes 3-5 business days. Need expedited shipping?",
                    "Your order will arrive in 3-5 days. Would you like to track your order?"
                ]
            },
            "return": {
                "patterns": [r".*\breturn\b.*", r".*\brefund\b.*", r".*\bexchange\b.*"],
                "responses": [
                    "You can return the product within 30 days of purchase. Need help with the return process?",
                    "Our refund policy allows returns within 30 days. Would you like to initiate a return?",
                    "Exchanges are available for unused items. Do you need assistance with an exchange?"
                ]
            },
            "warranty": {
                "patterns": [r".*\bwarranty\b.*", r".*\bguarantee\b.*", r".*\bcoverage\b.*"],
                "responses": [
                    "Our products come with a 1-year warranty. Would you like to extend it?",
                    "The warranty covers manufacturing defects. Need more details?",
                    "We offer a standard 1-year warranty. Are you interested in extended coverage?"
                ]
            },
            "support": {
                "patterns": [r".*\bsupport\b.*", r".*\bhelp\b.*", r".*\bcontact\b.*"],
                "responses": [
                    "We provide 24/7 customer support. How can I assist you today?",
                    "Our support team is available round the clock. What do you need help with?",
                    "You can reach us via phone, email, or chat. How can I help you?"
                ]
            }
        }

        # Match user message to intents
        for intent, data in intents.items():
            for pattern in data["patterns"]:
                if re.search(pattern, user_message):
                    return random.choice(data["responses"])

        # Fallback responses if no intent is matched
        fallback_responses = [
            "I'm here to assist you with your purchase! Could you provide more details?",
            "We have a wide range of products. Are you looking for recommendations?",
            "Could you specify the category or product you're interested in? I'd be happy to help!"
        ]

        return random.choice(fallback_responses)