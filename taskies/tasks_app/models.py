from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # PK autoincrement
    id = models.AutoField(primary_key=True)
    
    username = models.CharField(max_length=30, unique=True)

    # first_name - Default - Optional
    
    # last_name - Default - Optional
    
    # email - Default - Optional
    
    # password - Default - Needed
    
    # is_staff - Default - Automatically created
     
    # is_active - Default - Automatically created
    
    # date_joined - Default - Automatically created

    # is_superuser - Default - Automatically created
    
    # Role ( ENUM )
    WORKER = 'Worker'
    MANAGER = 'Manager'
    ROLE_CHOICES = [
        (WORKER, 'Worker'),
        (MANAGER, 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Username is the field for authentication 
    USERNAME_FIELD = 'username'

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