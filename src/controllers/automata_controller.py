# automata_controller.py - Controlador principal
from src.models.automata import AFND
from src.models.validator import ValidadorAutomata
from src.views.diagram_viewer import DiagramViewer

class AutomataController:
    def __init__(self, view):
        self.view = view
        self.afnd = None
        self.afd = None
        self.datos_basicos_validados = False
        self.estados = None
        self.simbolos = None
        self.estado_inicial = None
        self.estados_finales = None
    
    def validar_datos_basicos(self):
        """Primera parte: Validar datos básicos"""
        try:
            datos = self.view.get_datos_entrada()
            
            # Validar datos básicos
            self.estados, self.simbolos, self.estado_inicial, self.estados_finales = \
                ValidadorAutomata.validar_datos_basicos(
                    datos['estados'], 
                    datos['simbolos'], 
                    datos['inicial'], 
                    datos['finales']
                )
            
            self.datos_basicos_validados = True
            self.view.mostrar_resultado("✅ Datos básicos validados correctamente. Puede continuar con las transiciones.", "green")
            self.view.habilitar_transiciones()
            
        except ValueError as e:
            self.view.mostrar_error(str(e))
            self.datos_basicos_validados = False
    
    def validar_afnd(self):
        """Segunda parte: Validar AFND completo"""
        if not self.datos_basicos_validados:
            self.view.mostrar_error("Primero debe validar los datos básicos")
            return
            
        try:
            datos = self.view.get_datos_entrada()
            
            # Validar transiciones
            transiciones = ValidadorAutomata.validar_transiciones(
                datos['transiciones'], 
                self.estados, 
                self.simbolos
            )
            
            # Crear AFND
            self.afnd = AFND(
                self.estados, 
                self.simbolos, 
                transiciones, 
                self.estado_inicial, 
                self.estados_finales
            )
            
            # Verificar si es no determinístico
            if self.afnd.es_no_deterministico():
                self.view.mostrar_resultado("✅ El autómata es NO DETERMINÍSTICO", "green")
                # Habilitar botones
                self.view.habilitar_botones_afnd()
            else:
                self.view.mostrar_resultado("⚠️ El autómata ya es DETERMINÍSTICO", "orange")
                # Habilitar botones
                self.view.habilitar_botones_afnd()
                
        except ValueError as e:
            self.view.mostrar_error(str(e))
    
    def convertir_afd(self):
        if not self.afnd:
            self.view.mostrar_error("Primero debe validar el AFND completo")
            return
        
        # Solicitar secuencia mediante ventana emergente
        secuencia = self.view.solicitar_secuencia()
        if not secuencia:
            return  # Usuario canceló
        
        try:
            self.afd = self.afnd.convertir_a_afd()
            self.view.mostrar_resultado(f"✅ Conversión completada. Secuencia: {secuencia} - Estados AFD: {len(self.afd.estados)}", "blue")
            # Mostrar tabla de conversión
            self.view.mostrar_tabla_conversion_afd(self.afd)
            # Habilitar botón de mostrar AFD
            self.view.habilitar_boton_afd()
        except Exception as e:
            self.view.mostrar_error(f"Error en la conversión: {str(e)}")
    
    def mostrar_afnd(self):
        if not self.afnd:
            self.view.mostrar_error("Primero debe validar el AFND completo")
            return
        
        DiagramViewer.dibujar_diagrama_afnd(self.afnd, "AFND Original")
    
    def mostrar_afd(self):
        if not self.afd:
            self.view.mostrar_error("Primero debe convertir a AFD")
            return
        
        DiagramViewer.dibujar_diagrama_burbuja(self.afd, "AFD Convertido - Diagrama de Burbuja")
    
    def reset(self):
        """Resetea todos los datos del controlador"""
        self.afnd = None
        self.afd = None
        self.datos_basicos_validados = False
        self.estados = None
        self.simbolos = None
        self.estado_inicial = None
        self.estados_finales = None