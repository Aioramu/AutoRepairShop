import pytest
from authorization.models import User
from django.core import exceptions
from django.db import IntegrityError
username='test'
password='TEst2Pasw'
@pytest.fixture
def user_add():
    User.objects.create_user(username,password)
@pytest.mark.django_db(transaction=True)
def test_my_user(user_add):
    assert User.objects.all().count()!=0
    with pytest.raises(IntegrityError) as e_info:
        User.objects.create_user(username,password)
    me=User.objects.get(username=username)
    me.last_name="Testman"
    me.save()
    assert me.last_name=="Testman"
    assert User.objects.create_superuser(username+username,password).pk!=me.pk
@pytest.mark.django_db(transaction=True)
def test_registration_serializer(user_add):
    from authorization.serializers import RegistrationSerializer
    data={"username":"test","password":password,"password2":password}
    serializer = RegistrationSerializer(data=data)
    assert serializer.is_valid()==False

    data={"username":"Test","password":password,"password2":password}
    serializer = RegistrationSerializer(data=data)
    assert serializer.is_valid()==True
    user=serializer.save()

    data={"last_name":"lEcto"}
    serializer = RegistrationSerializer(user,data=data,partial=True)
    assert serializer.is_valid()==False
    data={"last_name":"*"*256}
    serializer = RegistrationSerializer(user,data=data,partial=True)
    assert serializer.is_valid()==False

    data={"last_name":"Sam-Abraham"}
    serializer = RegistrationSerializer(user,data=data,partial=True)
    assert serializer.is_valid()==True
    user=serializer.save()
    data={"auto_mark":"Kia"}
    serializer = RegistrationSerializer(user,data=data,partial=True)
    assert serializer.is_valid()==True
    user=serializer.save()
    data={"first_name":"Keanu2"}
    serializer = RegistrationSerializer(user,data=data,partial=True)
    assert serializer.is_valid()==False
    
    data['middle_name']="Sam-Abraham2"
    serializer = RegistrationSerializer(user,data=data,partial=True)
    assert serializer.is_valid()==False
