import matplotlib.pyplot as plt
import networkx as nx
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
    
    def epsilon_clausura(self, estados):
        """Calcula la epsilon-clausura de un conjunto de estados"""
        clausura = set(estados)
        pila = list(estados)
        
        while pila:
            estado = pila.pop()
            epsilon_trans = self.transiciones.get((estado, 'ε'), set())
            for destino in epsilon_trans:
                if destino not in clausura:
                    clausura.add(destino)
                    pila.append(destino)
        
        return clausura
    
    def convertir_a_afd(self):
        """Convierte AFND a AFD usando construcción de subconjuntos"""
        # Estado inicial del AFD
        q0_afd = frozenset(self.epsilon_clausura({self.estado_inicial}))
        
        estados_afd = {q0_afd}
        transiciones_afd = {}
        estados_finales_afd = set()
        
        # Cola para procesar estados
        cola = deque([q0_afd])
        
        while cola:
            estado_actual = cola.popleft()
            
            # Verificar si es estado final
            if any(e in self.estados_finales for e in estado_actual):
                estados_finales_afd.add(estado_actual)
            
            # Para cada símbolo del alfabeto
            for simbolo in self.alfabeto:
                if simbolo == 'ε':
                    continue
                    
                # Calcular destinos
                destinos = set()
                for estado in estado_actual:
                    destinos.update(self.transiciones.get((estado, simbolo), set()))
                
                if destinos:
                    # Aplicar epsilon-clausura
                    nuevo_estado = frozenset(self.epsilon_clausura(destinos))
                    
                    # Agregar transición
                    transiciones_afd[(estado_actual, simbolo)] = nuevo_estado
                    
                    # Si es nuevo estado, agregarlo a la cola
                    if nuevo_estado not in estados_afd:
                        estados_afd.add(nuevo_estado)
                        cola.append(nuevo_estado)
        
        return AFD(estados_afd, self.alfabeto, transiciones_afd, q0_afd, estados_finales_afd)
    
    def dibujar_diagrama(self, titulo="AFND"):
        """Dibuja el diagrama del autómata"""
        G = nx.MultiDiGraph()
        
        # Agregar nodo de inicio
        G.add_node('inicio', shape='box')
        
        # Agregar nodos del autómata
        for estado in self.estados:
            G.add_node(estado)
        
        # Agregar flecha de inicio
        G.add_edge('inicio', self.estado_inicial, label='')
        
        # Agregar aristas - cada transición como arista separada
        for (origen, simbolo), destinos in self.transiciones.items():
            for destino in destinos:
                G.add_edge(origen, destino, label=simbolo, key=f"{origen}-{simbolo}-{destino}")
        
        plt.figure(figsize=(12, 10))
        
        # Posicionamiento manual en cuadrícula como la imagen
        pos = {}
        estados_ordenados = sorted(self.estados)
        
        # Layout basado en la imagen: estructura 2x2 con inicio a la izquierda
        if len(estados_ordenados) >= 4:
            # Para 4 o más estados: estructura 2x2
            pos['inicio'] = (0, 1)  # Izquierda, centro vertical
            pos[estados_ordenados[0]] = (2, 1)  # A - centro izquierda
            pos[estados_ordenados[1]] = (4, 2)  # B - arriba derecha  
            pos[estados_ordenados[2]] = (2, 0)  # C - abajo izquierda
            pos[estados_ordenados[3]] = (4, 0)  # D - abajo derecha
            
            # Estados adicionales en línea
            for i, estado in enumerate(estados_ordenados[4:]):
                pos[estado] = (6 + i * 2, 1)
        else:
            # Para menos de 4 estados: layout simple
            pos['inicio'] = (0, 0)
            for i, estado in enumerate(estados_ordenados):
                if i == 0:
                    pos[estado] = (2, 0)
                elif i == 1:
                    pos[estado] = (4, 1)
                else:
                    pos[estado] = (2 + i * 2, -1)
        
        # Dibujar nodo de inicio
        nx.draw_networkx_nodes(G, pos, nodelist=['inicio'], 
                              node_color='lightgray', node_size=600, node_shape='s')
        
        # Dibujar todos los estados normales (sin color)
        estados_normales = self.estados - self.estados_finales
        nx.draw_networkx_nodes(G, pos, nodelist=estados_normales, 
                              node_color='lightgray', node_size=800)
        
        # Dibujar solo estados de aceptación con color
        nx.draw_networkx_nodes(G, pos, nodelist=self.estados_finales, 
                              node_color='lightgreen', node_size=800)
        
        # Dibujar aristas con curvaturas para separar múltiples transiciones
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, 
                              arrowsize=20, arrowstyle='->', connectionstyle="arc3,rad=0.1")
        
        # Etiquetas de nodos
        labels = {estado: estado for estado in self.estados}
        labels['inicio'] = 'inicio'
        nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold')
        
        # Dibujar etiquetas manualmente para cada arista
        for (origen, simbolo), destinos in self.transiciones.items():
            for destino in destinos:
                if origen != 'inicio':
                    # Calcular posición de la etiqueta
                    x1, y1 = pos[origen]
                    x2, y2 = pos[destino]
                    
                    # Posición de etiquetas mejorada
                    if origen == destino:  # Loop
                        # Posicionar etiqueta arriba del loop
                        label_x = x1
                        label_y = y1 + 0.2
                    else:
                        # Calcular posición en el medio de la arista
                        label_x = (x1 + x2) / 2
                        label_y = (y1 + y2) / 2
                        
                        # Ajustar posición según dirección de la flecha
                        dx = x2 - x1
                        dy = y2 - y1
                        
                        # Offset perpendicular para separar etiquetas
                        if abs(dx) > abs(dy):  # Flecha más horizontal
                            if simbolo == '0':
                                label_y += 0.15
                            else:
                                label_y -= 0.15
                        else:  # Flecha más vertical
                            if simbolo == '0':
                                label_x += 0.15
                            else:
                                label_x -= 0.15
                    
                    plt.text(label_x, label_y, simbolo, fontsize=10, 
                            ha='center', va='center', 
                            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        
        plt.title(titulo, size=16, weight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

class AFD:
    def __init__(self, estados, alfabeto, transiciones, estado_inicial, estados_finales):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales
    
    def dibujar_diagrama(self, titulo="AFD"):
        """Dibuja el diagrama del AFD"""
        G = nx.DiGraph()
        
        # Agregar nodo de inicio
        G.add_node('inicio')
        
        # Crear etiquetas legibles para los estados
        estado_labels = {}
        estados_ordenados = sorted(self.estados, key=lambda x: (x != self.estado_inicial, str(x)))
        
        for i, estado in enumerate(estados_ordenados):
            if isinstance(estado, frozenset):
                contenido = ','.join(sorted(estado))
                letra = chr(ord('A') + i)
                estado_labels[estado] = f"{letra}\n{{{contenido}}}"
            else:
                estado_labels[estado] = str(estado)
        
        estado_labels['inicio'] = 'inicio'
        
        # Agregar nodos
        for estado in self.estados:
            G.add_node(estado)
        
        # Agregar flecha de inicio
        G.add_edge('inicio', self.estado_inicial)
        
        # Agregar aristas
        for (origen, simbolo), destino in self.transiciones.items():
            G.add_edge(origen, destino, label=simbolo)
        
        plt.figure(figsize=(12, 10))
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Ajustar posición del nodo inicio
        if self.estado_inicial in pos:
            inicio_x = pos[self.estado_inicial][0] - 0.4
            inicio_y = pos[self.estado_inicial][1]
            pos['inicio'] = (inicio_x, inicio_y)
        
        # Dibujar nodo de inicio
        nx.draw_networkx_nodes(G, pos, nodelist=['inicio'], 
                              node_color='lightgray', node_size=1000, node_shape='s')
        
        # Dibujar todos los estados normales (sin color)
        estados_normales = self.estados - self.estados_finales
        nx.draw_networkx_nodes(G, pos, nodelist=estados_normales, 
                              node_color='lightgray', node_size=1500)
        
        # Dibujar solo estados de aceptación con color
        nx.draw_networkx_nodes(G, pos, nodelist=self.estados_finales, 
                              node_color='lightgreen', node_size=1500)
        
        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, 
                              arrowsize=20, arrowstyle='->')
        
        # Etiquetas de nodos
        nx.draw_networkx_labels(G, pos, estado_labels, font_size=8, font_weight='bold')
        
        # Etiquetas de aristas - cada transición por separado
        edge_labels = {}
        for (origen, simbolo), destino in self.transiciones.items():
            key = (origen, destino)
            if key in edge_labels:
                edge_labels[key] += f",{simbolo}"
            else:
                edge_labels[key] = simbolo
        
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10)
        
        plt.title(titulo, size=16, weight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

def ingresar_automata():
    """Función para ingresar el autómata desde consola"""
    print("=== CONVERTIDOR AFND A AFD ===\n")
    
    # Ingresar estados
    estados = input("Ingrese los estados separados por comas (A-Z, ej: A,B,C): ").split(',')
    estados = [e.strip().upper() for e in estados]
    
    # Validar estados
    for estado in estados:
        if not estado.isalpha() or len(estado) != 1:
            print(f"Error: '{estado}' no es válido. Use letras A-Z")
            return ingresar_automata()
    
    # Símbolos de entrada fijos
    alfabeto = ['0', '1', 'ε']
    print(f"Símbolos de entrada: {alfabeto}")
    
    # Ingresar estado inicial
    estado_inicial = input("Ingrese el estado inicial: ").strip()
    
    # Ingresar estados de aceptación
    estados_finales = input("Ingrese los estados de aceptación separados por comas: ").split(',')
    estados_finales = [e.strip().upper() for e in estados_finales]
    
    # Ingresar transiciones
    print("\nIngrese las transiciones en formato: estado_origen,simbolo,estado_destino")
    print("Para múltiples destinos use: estado_origen,simbolo,destino1;destino2")
    print("Escriba 'fin' para terminar:")
    
    transiciones = defaultdict(set)
    while True:
        trans = input("Transición: ").strip()
        if trans.lower() == 'fin':
            break
        
        try:
            origen, simbolo, destinos = trans.split(',')
            origen = origen.strip()
            simbolo = simbolo.strip()
            
            # Manejar múltiples destinos
            if ';' in destinos:
                destinos_list = [d.strip() for d in destinos.split(';')]
            else:
                destinos_list = [destinos.strip()]
            
            for destino in destinos_list:
                transiciones[(origen, simbolo)].add(destino)
                
        except ValueError:
            print("Formato incorrecto. Use: origen,simbolo,destino")
    
    return AFND(estados, alfabeto, transiciones, estado_inicial, estados_finales)

def main():
    # Ingresar autómata
    afnd = ingresar_automata()
    
    # Validar si es no determinístico
    if not afnd.es_no_deterministico():
        print("\n⚠️  El autómata ingresado ya es determinístico!")
        respuesta = input("¿Desea continuar con la conversión? (s/n): ")
        if respuesta.lower() != 's':
            return
    else:
        print("\n✅ El autómata es no determinístico. Procediendo con la conversión...")
    
    # Mostrar AFND original
    print("\n📊 Mostrando diagrama del AFND original...")
    afnd.dibujar_diagrama("AFND Original")
    
    # Convertir a AFD
    print("\n🔄 Convirtiendo AFND a AFD...")
    afd = afnd.convertir_a_afd()
    
    # Mostrar AFD resultante
    print("\n📊 Mostrando diagrama del AFD resultante...")
    afd.dibujar_diagrama("AFD Convertido")
    
    print("\n✅ Conversión completada exitosamente!")
    print(f"Estados AFD: {len(afd.estados)}")
    print(f"Estados de aceptación AFD: {len(afd.estados_finales)}")

if __name__ == "__main__":
    main()