from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from datetime import datetime,timedelta
import jwt
from django.conf import settings
# Create your models here.
class Marks(models.Model):
    mark=models.CharField(max_length=50,unique=True)

class User(AbstractBaseUser, PermissionsMixin):
    username=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=256)
    first_name=models.CharField(max_length=255,null=True,default=None)
    last_name=models.CharField(max_length=255,null=True,default=None)
    middle_name=models.CharField(max_length=255,null=True,default=None)
    auto_mark=models.ForeignKey(Marks,on_delete=models.SET_NULL,to_field="mark",null=True,default=None)
    #is_specialist=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()


    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.last_name+' '+self.first_name+' '+self.middle_name

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 360 days into the future.
        """
        dt = datetime.now() + timedelta(days=360)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
