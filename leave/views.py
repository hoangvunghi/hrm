from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from base.models import UserAccount,Leave
from .serializers import LeaveSerializer
# Create your views here.

@api_view(['DELETE'])
def delete_leave(request, pk):
    try:
        leave = Leave.objects.get(leave_id=pk)
    except Leave.DoesNotExist:
        return Response({"message": "Leave not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        leave_id = leave.leave_id
        if leave_id is not None and not UserAccount.objects.filter(user_id=leave_id).exists():
            return Response({"error": "Leave not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        leave.delete()
        return Response({"message": "Leave deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def create_leave(request):
    if request.method == 'POST':
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            leave_id = request.data.get('leave_id', None) 
            if leave_id is not None and not Leave.objects.filter(leave_id=leave_id).exists():
                return Response({"error": "Leave not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_leave(request, pk):
    try:
        leave = Leave.objects.get(leave_id=pk)
    except Leave.DoesNotExist:
        return Response({"message": "Leave not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = LeaveSerializer(leave, data=request.data)
        if serializer.is_valid():
            leave_id = request.data.get('leave_id', None) 
            if leave_id is not None and not Leave.objects.filter(leave_id=leave_id).exists():
                return Response({"error": "Leave not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)