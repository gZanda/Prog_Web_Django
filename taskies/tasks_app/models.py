from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('An email is required.')
        if not password:
            raise ValueError('A password is required.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', 'Manager')
        
        if not email:
            raise ValueError('An email is required.')
        if not password:
            raise ValueError('A password is required.')
        
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    # PK autoincrement
    id = models.AutoField(primary_key=True)
    
    # Email 
    email = models.EmailField(max_length=100, unique= True)

    # Name
    username = models.CharField(max_length=100)

    # Role ( ENUM )
    WORKER = 'Worker'
    MANAGER = 'Manager'
    ROLE_CHOICES = [
        (WORKER, 'Worker'),
        (MANAGER, 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default= 'Worker')

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AppUserManager()
    def __str__(self):
        return self.username

class Task(models.Model):
    # PK autoincrement
    id = models.AutoField(primary_key=True)

    # Description
    description = models.CharField(max_length=100)

    # Status (ENUM)
    PENDENTE = 'Pendente'
    PRONTA = 'Pronta'
    STATUS_CHOICES = [
        (PENDENTE, 'Pendente'),
        (PRONTA, 'Pronta'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    # Approval_Status (ENUM)
    APROVADA = 'Aprovada'
    REJEITADA = 'Rejeitada'
    NAO_AVALIADA = 'Não Avaliada'
    APPROVAL_STATUS_CHOICES = [
        (APROVADA, 'Aprovada'),
        (REJEITADA, 'Rejeitada'),
        (NAO_AVALIADA, 'Não Avaliada'),
    ]
    approval_status = models.CharField(max_length=15, choices=APPROVAL_STATUS_CHOICES)

    # Foreign Key -> Relate to User id
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)

    def __str__(self):
        return self.description