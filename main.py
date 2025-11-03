# main.py - Punto de entrada principal
import tkinter as tk
from src.views.main_window import AutomataView
from src.controllers.automata_controller import AutomataController

def main():
    # Crear ventana principal
    root = tk.Tk()
    
    # Crear vista
    view = AutomataView(root)
    
    # Crear controlador
    controller = AutomataController(view)
    
    # Conectar vista con controlador
    view.set_controller(controller)
    
    # Iniciar aplicación
    root.mainloop()

if __name__ == "__main__":
    main()