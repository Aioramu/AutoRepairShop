from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from .models import Record
from .serializers import RecordSerializer
from rest_framework import generics
from rest_framework.response import Response


class RecordsView(generics.GenericAPIView):
    queryset = Record.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = RecordSerializer
    def post(self,request):
        data=request.data.copy()
        data['client']=request.user.pk
        print(data)
        serializer=self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    def get(self,request):
        queryset=self.get_queryset().order_by('time')
        serializer=self.serializer_class(queryset,many=True)
        return Response(serializer.data)
