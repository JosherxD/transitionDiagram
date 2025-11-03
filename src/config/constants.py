# constants.py - Constantes de la aplicación
class AppConstants:
    # Configuración de ventana
    WINDOW_TITLE = "Convertidor AFND a AFD"
    WINDOW_SIZE = "800x600"
    WINDOW_PADDING = "10"
    
    # Configuración de campos
    ENTRY_WIDTH = 40
    TEXT_AREA_WIDTH = 50
    TEXT_AREA_HEIGHT = 8
    
    # Mensajes de la aplicación
    MESSAGES = {
        'basic_data_validated': "✅ Datos básicos validados correctamente. Puede continuar con las transiciones.",
        'nfa_detected': "✅ El autómata es NO DETERMINÍSTICO",
        'dfa_detected': "⚠️ El autómata ya es DETERMINÍSTICO",
        'conversion_completed': "✅ Conversión completada. Estados AFD: {count}",
        'validate_basic_first': "Primero debe validar los datos básicos",
        'validate_nfa_first': "Primero debe validar el AFND completo",
        'convert_first': "Primero debe convertir a AFD"
    }
    
    # Colores
    COLORS = {
        'success': 'green',
        'warning': 'orange',
        'info': 'blue',
        'error': 'red',
        'default': 'black'
    }
    
    # Etiquetas de la interfaz
    LABELS = {
        'states': "Estados (letras mayúsculas, ej: A,B,C):",
        'symbols': "Símbolos de entrada (números, ej: 0,1):",
        'initial_state': "Estado inicial:",
        'final_states': "Estados de Aceptación (ej: B,C):",
        'transitions': "Matriz de Transiciones:",
        'part2_title': "PARTE 2: MATRIZ DE TRANSICIONES"
    }
    
    # Botones
    BUTTONS = {
        'validate_basic': "Validar Datos Básicos",
        'reset': "Limpiar Datos",
        'validate_nfa': "Validar AFND",
        'convert': "Convertir a AFD",
        'show_nfa': "Mostrar AFND",
        'show_dfa': "Mostrar AFD"
    }