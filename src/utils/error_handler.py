# error_handler.py - Manejador centralizado de errores
import logging
from tkinter import messagebox

class ErrorHandler:
    @staticmethod
    def setup_logging():
        """Configura el sistema de logging"""
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('automata_errors.log'),
                logging.StreamHandler()
            ]
        )
    
    @staticmethod
    def handle_validation_error(error, context=""):
        """Maneja errores de validación"""
        message = f"Error de validación: {str(error)}"
        if context:
            message = f"{context} - {message}"
        
        logging.error(message)
        messagebox.showerror("Error de Validación", str(error))
    
    @staticmethod
    def handle_ui_error(error, context=""):
        """Maneja errores de interfaz"""
        message = f"Error de interfaz: {str(error)}"
        if context:
            message = f"{context} - {message}"
        
        logging.error(message)
        messagebox.showerror("Error de Interfaz", "Ha ocurrido un error en la interfaz. Consulte los logs para más detalles.")
    
    @staticmethod
    def handle_conversion_error(error, context=""):
        """Maneja errores de conversión de autómatas"""
        message = f"Error de conversión: {str(error)}"
        if context:
            message = f"{context} - {message}"
        
        logging.error(message)
        messagebox.showerror("Error de Conversión", f"Error al convertir el autómata: {str(error)}")
    
    @staticmethod
    def safe_execute(func, error_handler=None, context=""):
        """Ejecuta una función de forma segura con manejo de errores"""
        try:
            return func()
        except Exception as e:
            if error_handler:
                error_handler(e, context)
            else:
                ErrorHandler.handle_ui_error(e, context)
            return None