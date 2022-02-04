from rest_framework import serializers
from .models import Record
from authorization.serializers import RegistrationSerializer
import datetime
from authorization.models import User
from rest_framework import exceptions

class RecordSerializer(serializers.ModelSerializer):
    #client=RegistrationSerializer()
    class Meta:
        model = Record
        fields = '__all__'
        #fields = ('time','specialist','client')
    def validate_time(self,value):
        print(value.weekday())
        if value.hour<10 or value.hour>19:
                raise exceptions.ValidationError({"time": "In this time our service does not work"})
        elif value.hour==19 and value.minute!=00:
            raise exceptions.ValidationError({"time": "Diagnostics takes an hour, and the service closes at 20:00, please sign up for a time early"})
        if value.weekday()>=5:
            raise exceptions.ValidationError({"time": "Our service does not work at weekends"})
        return value
    def validate(self,attrs):
        """
        Check busy time for specialist,using range lookup because specialist works 1 hour per client thats equal 59 minutes in timedelta.
        """
        count=len(Record.objects.filter(time__range=[attrs['time']-datetime.timedelta(minutes=59),attrs['time']+datetime.timedelta(minutes=59)],specialist=attrs['specialist']))
        if count>0:
            raise exceptions.ValidationError({"time": "This time for this specialist is busy"})
        return attrs
