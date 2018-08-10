from .models import Key

def pending_keys(request):
    pending_keys = Key.objects.filter(current_status='new').count()
    return {'pending_keys': pending_keys}