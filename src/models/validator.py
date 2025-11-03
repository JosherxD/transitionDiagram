# validator.py - Validador de entrada
from collections import defaultdict

class ValidadorAutomata:
    @staticmethod
    def validar_estados(estados_str):
        if not estados_str:
            raise ValueError("Debe ingresar los estados")
        
        if ',' not in estados_str and len(estados_str.strip()) > 1:
            raise ValueError("Los estados deben estar separados por comas (,)")
        
        estados = [e.strip().upper() for e in estados_str.split(',')]
        for estado in estados:
            if not estado.isalpha() or len(estado) != 1:
                raise ValueError(f"Estado '{estado}' debe ser una letra mayúscula")
        return estados
    
    @staticmethod
    def validar_simbolos(simbolos_str):
        if not simbolos_str:
            raise ValueError("Debe ingresar los símbolos")
        
        simbolos = [s.strip() for s in simbolos_str.split(',')]
        
        if len(simbolos) != 2:
            raise ValueError("Debe ingresar exactamente 2 símbolos separados por coma")
        
        for simbolo in simbolos:
            if not simbolo.isdigit():
                raise ValueError(f"Símbolo '{simbolo}' debe ser un número")
        return simbolos
    
    @staticmethod
    def validar_estado_inicial(inicial_str, estados):
        if not inicial_str:
            raise ValueError("Debe ingresar el estado inicial")
        
        if ',' in inicial_str:
            raise ValueError("El estado inicial debe ser único (sin comas)")
        
        inicial = inicial_str.strip().upper()
        if inicial not in estados:
            raise ValueError("Estado inicial debe existir en los estados")
        
        return inicial
    
    @staticmethod
    def validar_estados_finales(finales_str, estados):
        if not finales_str:
            raise ValueError("Debe ingresar los estados de aceptación")
        
        if ',' not in finales_str and len(finales_str.strip()) > 1:
            raise ValueError("Los estados de aceptación deben estar separados por comas (,)")
        
        estados_finales = [e.strip().upper() for e in finales_str.split(',')]
        for estado in estados_finales:
            if estado not in estados:
                raise ValueError(f"Estado de aceptación '{estado}' debe existir en los estados")
        
        return estados_finales
    
    @staticmethod
    def validar_transiciones(trans_str, estados, simbolos):
        if not trans_str:
            raise ValueError("Debe ingresar las transiciones")
        
        transiciones = defaultdict(set)
        for linea in trans_str.split('\n'):
            if not linea.strip():
                continue
            
            partes = linea.strip().split(',')
            if len(partes) < 3:
                raise ValueError(f"Formato incorrecto en: {linea}. Use: origen,simbolo,destino")
            
            origen = partes[0]
            simbolo = partes[1]
            # Unir todas las partes restantes como destinos (pueden ser múltiples separados por comas)
            destinos_str = ','.join(partes[2:])
            origen = origen.strip().upper()
            simbolo = simbolo.strip()
            
            if origen not in estados:
                raise ValueError(f"Estado origen '{origen}' no existe")
            if simbolo not in simbolos:
                raise ValueError(f"Símbolo '{simbolo}' no existe")
            
            # Cambiar separador de ; a , para múltiples destinos
            destinos = [d.strip().upper() for d in destinos_str.split(',')]
            for destino in destinos:
                if destino not in estados:
                    raise ValueError(f"Estado destino '{destino}' no existe")
                transiciones[(origen, simbolo)].add(destino)
        
        return transiciones
    
    @staticmethod
    def validar_datos_basicos(estados_str, simbolos_str, inicial_str, finales_str):
        """Valida todos los datos básicos en una sola función"""
        # Convertir a mayúsculas automáticamente
        estados_str = estados_str.upper()
        inicial_str = inicial_str.upper()
        finales_str = finales_str.upper()
        
        estados = ValidadorAutomata.validar_estados(estados_str)
        simbolos = ValidadorAutomata.validar_simbolos(simbolos_str)
        inicial = ValidadorAutomata.validar_estado_inicial(inicial_str, estados)
        finales = ValidadorAutomata.validar_estados_finales(finales_str, estados)
        
        return estados, simbolos, inicial, finales