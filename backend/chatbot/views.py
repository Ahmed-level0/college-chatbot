from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from  .agent.agent import chat

# Create your views here.
class ChatView(APIView):
    def post(self, request):
        prompt = request.data.get('prompt', '')
        
        response = chat(prompt)
        
        return Response({'response': response})