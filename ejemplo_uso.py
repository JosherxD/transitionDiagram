from main import AFND
from collections import defaultdict

def ejemplo_afnd():
    """Ejemplo de uso con un AFND predefinido"""
    
    # Ejemplo: AFND que acepta cadenas que terminan en '01'
    estados = ['A', 'B', 'C']
    simbolos = ['0', '1']
    estado_inicial = 'A'
    estados_aceptacion = ['C']
    
    # Transiciones del AFND
    transiciones = defaultdict(set)
    transiciones[('A', '0')].add('A')  # Loop en A con '0'
    transiciones[('A', '1')].add('A')  # Loop en A con '1'
    transiciones[('A', '0')].add('B')  # Transición no determinística
    transiciones[('B', '1')].add('C')  # De B a C con '1'
    
    # Crear AFND
    afnd = AFND(estados, simbolos, transiciones, estado_inicial, estados_aceptacion)
    
    print("=== EJEMPLO DE CONVERSIÓN AFND A AFD ===")
    print("AFND que acepta cadenas que terminan en '01'\n")
    
    # Verificar si es no determinístico
    if afnd.es_no_deterministico():
        print("✅ El autómata es no determinístico")
    else:
        print("❌ El autómata es determinístico")
    
    # Mostrar AFND
    print("\n📊 Mostrando AFND original...")
    afnd.dibujar_diagrama("AFND - Termina en '01'")
    
    # Convertir a AFD
    print("🔄 Convirtiendo a AFD...")
    afd = afnd.convertir_a_afd()
    
    # Mostrar AFD
    print("📊 Mostrando AFD convertido...")
    afd.dibujar_diagrama("AFD - Termina en '01'")
    
    print("✅ Conversión completada!")

if __name__ == "__main__":
    ejemplo_afnd()