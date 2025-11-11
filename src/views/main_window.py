# main_window.py - Ventana principal
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from src.utils.input_validators import InputValidators
from src.utils.ui_helpers import UIHelpers
from src.utils.error_handler import ErrorHandler
from src.utils.ui_optimizer import UIOptimizer
from src.config.constants import AppConstants

class AutomataView:
    def __init__(self, root):
        self.root = root
        self.controller = None
        
        # Configurar logging
        ErrorHandler.setup_logging()
        
        # Inicializar interfaz con manejo de errores
        ErrorHandler.safe_execute(
            lambda: self._initialize_window(),
            ErrorHandler.handle_ui_error,
            "Inicializando ventana principal"
        )
    
    def _initialize_window(self):
        """Inicializa la configuración de la ventana"""
        self.root.title(AppConstants.WINDOW_TITLE)
        self.root.geometry(AppConstants.WINDOW_SIZE)
        self.crear_interfaz()
    
    def set_controller(self, controller):
        self.controller = controller
    
    def crear_interfaz(self):
        # Crear canvas y scrollbar para scroll vertical
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configurar scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Posicionar canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con mouse wheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        main_frame = ttk.Frame(self.scrollable_frame, padding=AppConstants.WINDOW_PADDING)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text=AppConstants.WINDOW_TITLE, font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(main_frame, text=AppConstants.LABELS['states']).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.estados_entry = ttk.Entry(main_frame, width=AppConstants.ENTRY_WIDTH)
        self.estados_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(main_frame, text=AppConstants.LABELS['symbols']).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.simbolos_entry = ttk.Entry(main_frame, width=AppConstants.ENTRY_WIDTH)
        self.simbolos_entry.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(main_frame, text=AppConstants.LABELS['initial_state']).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.inicial_entry = ttk.Entry(main_frame, width=AppConstants.ENTRY_WIDTH)
        self.inicial_entry.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(main_frame, text=AppConstants.LABELS['final_states']).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.finales_entry = ttk.Entry(main_frame, width=AppConstants.ENTRY_WIDTH)
        self.finales_entry.grid(row=4, column=1, pady=5, padx=5)
        
        # Botones para validar datos básicos y reset
        button_frame1 = ttk.Frame(main_frame)
        button_frame1.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame1, text=AppConstants.BUTTONS['validate_basic'], command=self.validar_datos_basicos).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame1, text=AppConstants.BUTTONS['reset'], command=self.reset_formulario).pack(side=tk.LEFT, padx=5)
        
        # Segunda parte - Transiciones (inicialmente oculta)
        self.separador = ttk.Separator(main_frame, orient='horizontal')
        
        self.titulo_parte2 = ttk.Label(main_frame, text=AppConstants.LABELS['part2_title'], font=("Arial", 12, "bold"))
        
        # Frame para la matriz de transiciones
        self.matriz_frame = ttk.Frame(main_frame)
        self.matriz_entries = {}  # Diccionario para almacenar las entradas de la matriz
        
        self.aceptacion_entries = {}  # Diccionario para las entradas de aceptación
        
        # Frame para la tabla de conversión AFD
        self.conversion_frame = ttk.Frame(main_frame)
        

        
        self.button_frame2 = ttk.Frame(main_frame)
        
        self.btn_validar_afnd = ttk.Button(self.button_frame2, text=AppConstants.BUTTONS['validate_nfa'], command=self.validar_afnd)
        self.btn_validar_afnd.pack(side=tk.LEFT, padx=5)
        
        self.btn_mostrar_afnd = ttk.Button(self.button_frame2, text=AppConstants.BUTTONS['show_nfa'], command=self.mostrar_afnd, state='disabled')
        self.btn_mostrar_afnd.pack(side=tk.LEFT, padx=5)
        
        self.btn_convertir = ttk.Button(self.button_frame2, text=AppConstants.BUTTONS['convert'], command=self.convertir_afd, state='disabled')
        self.btn_convertir.pack(side=tk.LEFT, padx=5)
        
        self.btn_mostrar_afd = ttk.Button(self.button_frame2, text=AppConstants.BUTTONS['show_dfa'], command=self.mostrar_afd, state='disabled')
        self.btn_mostrar_afd.pack(side=tk.LEFT, padx=5)
        
        self.btn_reset = ttk.Button(self.button_frame2, text=AppConstants.BUTTONS['reset'], command=self.reset_formulario)
        self.btn_reset.pack(side=tk.LEFT, padx=5)
        
        self.resultado_label = ttk.Label(main_frame, text="", font=("Arial", 12))
        
        # Inicialmente ocultar la segunda parte
        self.ocultar_segunda_parte()
        
        # Configurar validaciones usando helpers
        UIHelpers.setup_field_validation(self.root, self.estados_entry, InputValidators.validate_states)
        UIHelpers.setup_field_validation(self.root, self.simbolos_entry, InputValidators.validate_symbols)
        UIHelpers.setup_field_validation(self.root, self.inicial_entry, InputValidators.validate_initial_state)
        UIHelpers.setup_field_validation(self.root, self.finales_entry, InputValidators.validate_final_states)
        
        # Configurar conversión a mayúsculas
        UIHelpers.setup_uppercase_conversion(self.estados_entry)
        UIHelpers.setup_uppercase_conversion(self.inicial_entry)
        UIHelpers.setup_uppercase_conversion(self.finales_entry)
    
    def get_datos_entrada(self):
        return {
            'estados': self.estados_entry.get().strip(),
            'simbolos': self.simbolos_entry.get().strip(),
            'inicial': self.inicial_entry.get().strip(),
            'finales': self.finales_entry.get().strip(),
            'transiciones': self.get_transiciones_from_matriz()
        }
    
    def get_transiciones_from_matriz(self):
        """Convierte la matriz de transiciones a formato de texto"""
        transiciones = []
        if hasattr(self, 'estados_validados') and hasattr(self, 'simbolos_validados'):
            for estado in self.estados_validados:
                for simbolo in self.simbolos_validados:
                    key = f"{estado},{simbolo}"
                    if key in self.matriz_entries:
                        destinos = self.matriz_entries[key].get().strip()
                        if destinos:
                            transiciones.append(f"{estado},{simbolo},{destinos}")
        return '\n'.join(transiciones)
    
    def crear_matriz_transiciones(self, estados, simbolos):
        """Crea la matriz de transiciones basada en estados y símbolos"""
        # Limpiar matriz anterior
        for widget in self.matriz_frame.winfo_children():
            widget.destroy()
        self.matriz_entries.clear()
        
        # Guardar estados y símbolos validados
        self.estados_validados = estados
        self.simbolos_validados = simbolos
        
        # Crear encabezados
        ttk.Label(self.matriz_frame, text="Estados", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=2)
        ttk.Label(self.matriz_frame, text="Símbolos de entrada", font=("Arial", 10, "bold")).grid(row=0, column=1, columnspan=len(simbolos), padx=5, pady=2)
        ttk.Label(self.matriz_frame, text="Acepta(1)/Rechaza(0)", font=("Arial", 10, "bold")).grid(row=0, column=len(simbolos)+1, padx=5, pady=2)
        
        # Encabezados de símbolos
        for j, simbolo in enumerate(simbolos):
            ttk.Label(self.matriz_frame, text=simbolo, font=("Arial", 9, "bold")).grid(row=1, column=j+1, padx=2, pady=2)
        
        # Crear filas para cada estado
        for i, estado in enumerate(estados):
            # Etiqueta del estado
            ttk.Label(self.matriz_frame, text=estado, font=("Arial", 9)).grid(row=i+2, column=0, padx=5, pady=2, sticky=tk.W)
            
            # Entradas para cada símbolo
            for j, simbolo in enumerate(simbolos):
                key = f"{estado},{simbolo}"
                entry = ttk.Entry(self.matriz_frame, width=10)
                entry.grid(row=i+2, column=j+1, padx=2, pady=2)
                # Configurar validación y conversión a mayúsculas
                UIHelpers.setup_field_validation(self.root, entry, InputValidators.validate_matrix_cell)
                UIHelpers.setup_uppercase_conversion(entry)
                self.matriz_entries[key] = entry
            
            # Entrada para aceptación/rechazo (solo lectura)
            aceptacion_entry = ttk.Entry(self.matriz_frame, width=5, state='readonly')
            aceptacion_entry.grid(row=i+2, column=len(simbolos)+1, padx=2, pady=2)
            
            # Prellenar con 1 si es estado final, 0 si no
            valor = "1" if estado in self.controller.estados_finales else "0"
            aceptacion_entry.config(state='normal')
            aceptacion_entry.insert(0, valor)
            aceptacion_entry.config(state='readonly')
            
            self.aceptacion_entries[estado] = aceptacion_entry
    
    def mostrar_tabla_conversion_afd(self, afd):
        """Muestra la tabla de conversión del AFD"""
        def _crear_tabla():
            # Limpiar tabla anterior de forma segura
            UIOptimizer.safe_widget_destroy(self.conversion_frame)
            
            if not afd or not hasattr(afd, 'estados'):
                raise ValueError("AFD inválido o sin estados")
            
            self._crear_encabezados_tabla(afd)
            self._crear_filas_tabla(afd)
        
        ErrorHandler.safe_execute(
            _crear_tabla,
            ErrorHandler.handle_ui_error,
            "Creando tabla de conversión AFD"
        )
    
    def _crear_encabezados_tabla(self, afd):
        """Crea los encabezados de la tabla de conversión"""
        # Título
        ttk.Label(self.conversion_frame, text="CONVERTIR UN AUTOMATA FINITO NO DETERMINISTICO EN AUTOMATA FINITO DETERMINISTICO", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Encabezados
        ttk.Label(self.conversion_frame, text="ESTADOS", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Label(self.conversion_frame, text="SIMBOLOS DE ENTRADA", font=("Arial", 10, "bold")).grid(row=1, column=1, columnspan=2, padx=5, pady=2)
        ttk.Label(self.conversion_frame, text="ACEPTA/RECHAZA", font=("Arial", 10, "bold")).grid(row=1, column=3, padx=5, pady=2)
        
        # Subencabezados de símbolos
        simbolos = list(afd.alfabeto)
        for j, simbolo in enumerate(simbolos):
            ttk.Label(self.conversion_frame, text=simbolo, font=("Arial", 9, "bold")).grid(row=2, column=j+1, padx=5, pady=2)
    
    def _crear_filas_tabla(self, afd):
        """Crea las filas de datos de la tabla de conversión"""
        simbolos = list(afd.alfabeto)
        # Crear filas para cada estado del AFD
        row = 3
        for estado in sorted(afd.estados, key=str):
            self._crear_fila_estado(estado, simbolos, afd, row)
            row += 1
    
    def _crear_fila_estado(self, estado, simbolos, afd, row):
        """Crea una fila para un estado específico"""
        # Nombre del estado (convertir frozenset a string legible)
        estado_nombre = self._format_estado_nombre(estado)
        ttk.Label(self.conversion_frame, text=estado_nombre, font=("Arial", 9)).grid(row=row, column=0, padx=5, pady=2, sticky=tk.W)
        
        # Transiciones para cada símbolo
        for j, simbolo in enumerate(simbolos):
            destino = afd.transiciones.get((estado, simbolo), "ERROR")
            destino_nombre = self._format_estado_nombre(destino)
            ttk.Label(self.conversion_frame, text=destino_nombre, font=("Arial", 9)).grid(row=row, column=j+1, padx=5, pady=2)
        
        # Aceptación/Rechazo
        acepta = "1" if estado in afd.estados_finales else "0"
        ttk.Label(self.conversion_frame, text=acepta, font=("Arial", 9)).grid(row=row, column=3, padx=5, pady=2)
    
    def _format_estado_nombre(self, estado):
        """Formatea el nombre de un estado para mostrar"""
        if isinstance(estado, frozenset):
            return ''.join(sorted(estado)) if estado else "ERROR"
        elif estado == "ERROR" or estado is None:
            return "ERROR"
        else:
            return str(estado)
    
    def mostrar_resultado(self, mensaje, color="black"):
        self.resultado_label.config(text=mensaje, foreground=color)
    
    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)
    
    def validar_afnd(self):
        if self.controller:
            self.controller.validar_afnd()
    
    def convertir_afd(self):
        if self.controller:
            self.controller.convertir_afd()
    
    def mostrar_afnd(self):
        if self.controller:
            self.controller.mostrar_afnd()
    
    def mostrar_afd(self):
        if self.controller:
            self.controller.mostrar_afd()
    
    def validar_datos_basicos(self):
        """Valida los datos básicos antes de continuar"""
        if self.controller:
            self.controller.validar_datos_basicos()
    
    def ocultar_segunda_parte(self):
        """Oculta completamente la segunda parte"""
        # No hacer grid() de los widgets de la segunda parte
        pass
    
    def mostrar_segunda_parte(self):
        """Muestra la segunda parte y bloquea la primera"""
        # Mostrar separador y segunda parte
        self.separador.grid(row=6, column=0, columnspan=2, sticky='ew', pady=10)
        self.titulo_parte2.grid(row=7, column=0, columnspan=2, pady=5)
        self.matriz_frame.grid(row=8, column=0, columnspan=2, pady=10, padx=5)
        self.button_frame2.grid(row=9, column=0, columnspan=2, pady=20)
        self.conversion_frame.grid(row=10, column=0, columnspan=2, pady=10, padx=5)
        self.resultado_label.grid(row=11, column=0, columnspan=2, pady=10)
        
        # Bloquear campos de la primera parte
        self.estados_entry.config(state='readonly')
        self.simbolos_entry.config(state='readonly')
        self.inicial_entry.config(state='readonly')
        self.finales_entry.config(state='readonly')
    
    def habilitar_transiciones(self):
        """Habilita la sección de transiciones"""
        # Obtener datos validados del controlador
        if self.controller and hasattr(self.controller, 'estados') and hasattr(self.controller, 'simbolos'):
            self.crear_matriz_transiciones(self.controller.estados, self.controller.simbolos)
        self.mostrar_segunda_parte()
    
    def habilitar_botones_afnd(self):
        """Habilita los botones después de validar AFND"""
        self.btn_mostrar_afnd.config(state='normal')
        self.btn_convertir.config(state='normal')
    
    def habilitar_boton_afd(self):
        """Habilita el botón de mostrar AFD después de la conversión"""
        self.btn_mostrar_afd.config(state='normal')
    

    
    def reset_formulario(self):
        """Resetea todo el formulario"""
        def _reset_operation():
            if self.controller:
                self.controller.reset()
            
            # Limpiar campos principales de forma optimizada
            main_entries = [self.estados_entry, self.simbolos_entry, self.inicial_entry, self.finales_entry]
            UIOptimizer.configure_entries_state(main_entries, 'normal', 'none')
            UIOptimizer.clear_entries(main_entries)
            
            # Limpiar matriz si existe
            if hasattr(self, 'matriz_entries'):
                UIOptimizer.clear_entries(list(self.matriz_entries.values()))
            
            # Limpiar entradas de aceptación si existen
            if hasattr(self, 'aceptacion_entries'):
                self.aceptacion_entries.clear()
            
            # Limpiar tabla de conversión si existe
            if hasattr(self, 'conversion_frame'):
                UIOptimizer.safe_widget_destroy(self.conversion_frame)
            
            self._reactivar_validaciones()
            self._ocultar_elementos_segunda_parte()
        
        ErrorHandler.safe_execute(
            _reset_operation,
            ErrorHandler.handle_ui_error,
            "Reseteando formulario"
        )
    
    def _reactivar_validaciones(self):
        """Reactiva las validaciones de los campos principales"""
        validations = [
            (self.estados_entry, InputValidators.validate_states),
            (self.simbolos_entry, InputValidators.validate_symbols),
            (self.inicial_entry, InputValidators.validate_initial_state),
            (self.finales_entry, InputValidators.validate_final_states)
        ]
        
        for entry, validator in validations:
            UIHelpers.setup_field_validation(self.root, entry, validator)
        
        # Reactivar conversión a mayúsculas
        uppercase_entries = [self.estados_entry, self.inicial_entry, self.finales_entry]
        for entry in uppercase_entries:
            UIHelpers.setup_uppercase_conversion(entry)
    
    def _ocultar_elementos_segunda_parte(self):
        """Oculta los elementos de la segunda parte"""
        elementos = [
            self.separador, self.titulo_parte2, self.matriz_frame,
            self.button_frame2, self.conversion_frame, self.resultado_label
        ]
        
        for elemento in elementos:
            try:
                elemento.grid_remove()
            except:
                pass
        
        self.mostrar_resultado("", "black")

    
    def _on_mousewheel(self, event):
        """Maneja el scroll con la rueda del mouse"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")