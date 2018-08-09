class TraceabilityDatabaseRouter(object):
    """
    Determine how to route database calls for an app's models.
    All other models will be routed to the next router in the DATABASE_ROUTERS setting if applicable,
    or otherwise to the default database.
    """

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