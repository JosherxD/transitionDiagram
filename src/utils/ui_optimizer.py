# ui_optimizer.py - Optimizador de operaciones de UI
class UIOptimizer:
    @staticmethod
    def batch_widget_operation(widgets, operation, *args, **kwargs):
        """Ejecuta operaciones en lote sobre múltiples widgets"""
        for widget in widgets:
            if hasattr(widget, operation):
                getattr(widget, operation)(*args, **kwargs)
    
    @staticmethod
    def safe_widget_destroy(frame):
        """Destruye widgets de forma segura"""
        if hasattr(frame, 'winfo_children'):
            for widget in frame.winfo_children():
                try:
                    widget.destroy()
                except:
                    pass
    
    @staticmethod
    def configure_entries_state(entries, state, validate=None):
        """Configura el estado de múltiples entries de forma optimizada"""
        for entry in entries:
            if hasattr(entry, 'config'):
                config_dict = {'state': state}
                if validate is not None:
                    config_dict['validate'] = validate
                entry.config(**config_dict)
    
    @staticmethod
    def clear_entries(entries):
        """Limpia múltiples entries de forma optimizada"""
        for entry in entries:
            if hasattr(entry, 'delete'):
                try:
                    entry.delete(0, 'end')
                except:
                    pass