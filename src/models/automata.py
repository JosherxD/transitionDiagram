# automata.py - Modelos de autómatas
from collections import defaultdict, deque

class AFND:
    def __init__(self, estados, alfabeto, transiciones, estado_inicial, estados_finales):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_finales = set(estados_finales)
    
    def es_no_deterministico(self):
        """Verifica si el autómata es no determinístico"""
        for estado in self.estados:
            for simbolo in self.alfabeto:
                destinos = self.transiciones.get((estado, simbolo), set())
                if len(destinos) > 1:
                    return True
        return False
    
    def convertir_a_afd(self):
        """Convierte AFND a AFD usando construcción de subconjuntos"""
        q0_afd = frozenset({self.estado_inicial})
        
        estados_afd = {q0_afd}
        transiciones_afd = {}
        estados_finales_afd = set()
        cola = deque([q0_afd])
        tiene_error = False
        
        while cola:
            estado_actual = cola.popleft()
            
            if any(e in self.estados_finales for e in estado_actual):
                estados_finales_afd.add(estado_actual)
            
            for simbolo in self.alfabeto:
                destinos = set()
                for estado in estado_actual:
                    destinos.update(self.transiciones.get((estado, simbolo), set()))
                
                if destinos:
                    nuevo_estado = frozenset(destinos)
                    transiciones_afd[(estado_actual, simbolo)] = nuevo_estado
                    
                    if nuevo_estado not in estados_afd:
                        estados_afd.add(nuevo_estado)
                        cola.append(nuevo_estado)
                else:
                    # No hay transición, va a ERROR
                    transiciones_afd[(estado_actual, simbolo)] = "ERROR"
                    tiene_error = True
        
        # No agregar ERROR como estado, solo en transiciones
        
        return AFD(estados_afd, self.alfabeto, transiciones_afd, q0_afd, estados_finales_afd)

class AFD:
    def __init__(self, estados, alfabeto, transiciones, estado_inicial, estados_finales):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales