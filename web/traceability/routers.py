#Establece la configuración necesaria para no gestionar la base de datos de trazabilidad

class TraceabilityDatabaseRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'traceability':
            return 'traceability'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'traceability':
            return 'traceability'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'traceability' and obj2._meta.app_label == 'traceability':
            return True
        
        elif 'traceability' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None

        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'traceability' or db == 'example_db':
            return False

        return None