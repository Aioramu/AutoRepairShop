from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .models import User
from .serializers import RegistrationSerializer
from rest_framework import generics
from rest_framework.response import Response



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
class UpdateParamsView(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = RegistrationSerializer
    def put(self,request):
        queryset=self.queryset.get(pk=request.user.pk)
        serializer=self.serializer_class(queryset,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
