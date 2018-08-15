from django.db import models
from django.contrib.postgres.fields import JSONField
from django.urls import reverse

from Crypto.Hash import SHA256

# Create your models here.
class Key(models.Model):
    hash = models.CharField(max_length=64, primary_key=True)
    public_key = models.TextField('Clave Pública', max_length=300)
    status_choices = (('active', 'Activa'), ('inactive', 'Inactiva'), ('new', 'Pendiente de Aprobación'))
    current_status = models.CharField('Estado', max_length=8, choices=status_choices, default='new')
    name = models.CharField('Nombre', max_length=50)
    description = models.TextField('Descripción', max_length=300, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.hash = SHA256.new(self.public_key.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('key_details', kwargs={'hash': self.hash})

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'keys'

class Transaction(models.Model):
    hash = models.CharField(max_length=64, primary_key=True)
    type = models.IntegerField()
    mode = models.IntegerField()
    transmitter = models.ForeignKey(Key, on_delete=models.CASCADE, related_name='transmitter', db_column='transmitter')
    receiver = models.ForeignKey(Key, on_delete=models.CASCADE, related_name='receiver', db_column='receiver', null = True)
    server_timestamp = models.DateTimeField()
    client_timestamp = models.DateTimeField()
    transaction_data = JSONField()
    sign = models.CharField(max_length=256)
    updated_quantity = JSONField()

    class Meta:
        db_table = 'transactions'
        ordering = ('-client_timestamp',)
    
    def __str__(self):
        return self.hash