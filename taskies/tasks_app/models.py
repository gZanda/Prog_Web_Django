from django.db import models

class User(models.Model):
    # PK autoincrement
    id = models.AutoField(primary_key=True)
    
    # Name
    name = models.CharField(max_length=100)
    
    # Role ( ENUM )
    WORKER = 'Worker'
    MANAGER = 'Manager'
    ROLE_CHOICES = [
        (WORKER, 'Worker'),
        (MANAGER, 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name

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