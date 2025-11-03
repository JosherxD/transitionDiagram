# ui_helpers.py - Funciones auxiliares para la interfaz
import tkinter as tk

class UIHelpers:
    @staticmethod
    def convert_to_uppercase(event):
        """Convierte a mayúsculas sin borrar el contenido"""
        widget = event.widget
        current_pos = widget.index(tk.INSERT)
        current_text = widget.get()
        upper_text = current_text.upper()
        
        if current_text != upper_text:
            widget.delete(0, tk.END)
            widget.insert(0, upper_text)
            widget.icursor(current_pos)
    
    @staticmethod
    def setup_field_validation(root, entry_widget, validator_func):
        """Configura validación para un campo de entrada"""
        vcmd = (root.register(validator_func), '%P')
        entry_widget.config(validate='key', validatecommand=vcmd)
    
    @staticmethod
    def setup_uppercase_conversion(entry_widget):
        """Configura conversión automática a mayúsculas"""
        entry_widget.bind('<KeyRelease>', UIHelpers.convert_to_uppercase)
    
    @staticmethod
    def clear_widget_grid(widget):
        """Oculta un widget del grid"""
        widget.grid_remove()
    
    @staticmethod
    def show_widget_grid(widget, row, column, **kwargs):
        """Muestra un widget en el grid"""
        widget.grid(row=row, column=column, **kwargs)