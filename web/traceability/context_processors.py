from .models import Key

def pending_keys(request):
    pending_keys = Key.objects.filter(active=False).count()
    return {'pending_keys': pending_keys}