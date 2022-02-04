import pytest
from authorization.models import User
from django.core import exceptions
from diagnostics.models import Record
from authorization.tests.registration_tests import user_add

@pytest.fixture
def record_add(user_add):
    user=User.objects.last()
    Record.objects.create(time="2023-02-14 11:00",client=user,specialist='suspension')


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('time,result',[('2023-02-14 11:00',False),('2023-02-14 12:01',True),
('2023-02-14 10:00',True),('2023-02-18 10:00',False),('2023-02-14 12:30',True),
('2023-02-14 19:01',False),('2023-02-14 20:00',False),('2023-02-14 11:59',False)])
def test_time(user_add,record_add,time,result):
    from diagnostics.serializers import RecordSerializer
    user=User.objects.last().pk
    data={
    "time":time,
    "client":user,
    "specialist":'suspension'
    }
    serializer=RecordSerializer(data=data)
    assert serializer.is_valid()==result
@pytest.mark.django_db(transaction=True)
def test_specialist(user_add,record_add):
    from diagnostics.serializers import RecordSerializer
    user=User.objects.last().pk
    data={
    "time":"2022-02-14 11:00",
    "client":user,
    "specialist":'universal'
    }
    serializer=RecordSerializer(data=data)
    assert serializer.is_valid()==True
