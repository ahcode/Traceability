from django.db import models

# Create your models here.
class Key(models.Model):
    hash = models.CharField(max_length=64, primary_key=True)
    public_key = models.TextField(max_length=300)
    status_choices = (('active', 'Activa'), ('inactive', 'Inactiva'), ('new', 'Pendiente de Aprobación'))
    current_status = models.CharField(max_length=8, choices=status_choices, default='new')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300)

    def __str__():
        return name

    class Meta:
        db_table = 'keys'