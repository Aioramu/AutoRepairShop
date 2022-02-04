from rest_framework import serializers
from .models import User,Marks
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import exceptions

class CreatableSlugRelatedField(serializers.SlugRelatedField):#to create field if not exist

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    auto_mark=CreatableSlugRelatedField(queryset=Marks.objects.all(),
        slug_field='mark',allow_null=True,required=False)
    class Meta:
        model = User
        fields = ('username', 'password','password2','first_name','last_name','middle_name','auto_mark')

    def validate(self, attrs):
        if 'password' in attrs and 'password2' in attrs:
            if attrs['password'] != attrs['password2']:
                raise exceptions.ValidationError({"password": "Password fields didn't match."})
        return attrs
    def char_validate(self,value,key):
        #print(value.find("-"), value[value.find("-")+1:])
        if value.isalpha() !=True:
            if "-" not in value:#check for double-named person
                raise exceptions.ValidationError({key: "field must contain characters only"})
            elif value[:value.find("-")].istitle() and value[:value.find("-")].isalpha():
                if value[value.find("-")+1:].istitle() and value[value.find("-")+1:].isalpha():
                    return value
                else:
                    raise exceptions.ValidationError({key: "Please declare your dual name in capital letters"})
        if value.istitle() !=True:
            raise exceptions.ValidationError({key: "field must be title!"})
        return value
    def validate_first_name(self, value):
        value=self.char_validate(value,"first_name")
        return value
    def validate_last_name(self, value):
        value=self.char_validate(value,"first_name")
        return value
    def validate_middle_name(self, value):
        value=self.char_validate(value,"first_name")
        return value
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.pop('username'),password=validated_data.pop('password'))
        validated_data.pop('password2')
        for i in validated_data:
            setattr(user,i,validated_data[i])
            user.save()
        return user
    def update(self,instance,validated_data):
        for i in validated_data:
            setattr(instance,i,validated_data[i])
            instance.save()
        return instance
