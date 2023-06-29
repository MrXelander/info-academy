from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nc = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role', 'nc', 'password']

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        names = self.first_name.split()
        return names[0] if names else ''

class Materia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
class Tema(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre