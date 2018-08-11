from django.db import models
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

    def __str__():
        return name

    class Meta:
        db_table = 'keys'