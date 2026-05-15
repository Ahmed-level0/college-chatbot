from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from  .agent.agent import chat

# Create your views here.
class ChatView(APIView):

    def post(self, request):
        prompt = request.data.get("prompt")

        if not prompt:
            return Response(
                {"error": "Prompt is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            response = chat(prompt)

            return Response({
                "response": response
            })

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )