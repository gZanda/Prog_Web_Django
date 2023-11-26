from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # PK autoincrement
    id = models.AutoField(primary_key=True)
    
    username = models.CharField(max_length=30, unique=True)
    
    email = models.EmailField(max_length=254, unique=True)
    
    # password - Comes by default - Needed for authentication
    
    # Role ( ENUM )
    WORKER = 'Worker'
    MANAGER = 'Manager'
    ROLE_CHOICES = [
        (WORKER, 'Worker'),
        (MANAGER, 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # email is the field for autheentication
    USERNAME_FIELD = 'email'

    # Required fields
    REQUIRED_FIELDS = ['username','password', 'role']

    def __str__(self):
        return self.username

class Task(models.Model):
    # PK autoincrement
    id = models.AutoField(primary_key=True)

    # Description
    description = models.CharField(max_length=300)

    # Status (ENUM)
    PENDENTE = 'Pendente'
    PRONTA = 'Pronta'
    STATUS_CHOICES = [
        (PENDENTE, 'Pendente'),
        (PRONTA, 'Pronta'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDENTE)

    # Approval_Status (ENUM)
    APROVADA = 'Aprovada'
    REJEITADA = 'Rejeitada'
    NAO_AVALIADA = 'Não Avaliada'
    APPROVAL_STATUS_CHOICES = [
        (APROVADA, 'Aprovada'),
        (REJEITADA, 'Rejeitada'),
        (NAO_AVALIADA, 'Não Avaliada'),
    ]
    approval_status = models.CharField(max_length=15, choices=APPROVAL_STATUS_CHOICES, default=NAO_AVALIADA)

    # Foreign Key -> Relate to User id
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)

    def __str__(self):
        return self.description