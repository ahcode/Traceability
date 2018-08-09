from django.db import models

# Create your models here.
class Key(models.Model):
    hash = models.CharField(max_length=64, primary_key=True)
    public_key = models.TextField(max_length=300)
    active = models.BooleanField(default = False)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300)

    def __str__():
        return name

    class Meta:
        db_table = 'keys'