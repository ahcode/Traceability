from .models import Key

#Obtiene el número de claves en estado pendiente de activación
def pending_keys(request):
    pending_keys = Key.objects.filter(current_status='new').count()
    return {'pending_keys': pending_keys}