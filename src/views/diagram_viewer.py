# diagram_viewer.py - Visualizador de diagramas
import matplotlib.pyplot as plt
import networkx as nx
from src.utils.diagram_utils import DiagramUtils

class DiagramViewer:
    @staticmethod
    def dibujar_diagrama_afnd(automata, titulo):
        G = nx.MultiDiGraph()
        G.add_node('inicio')
        
        for estado in automata.estados:
            G.add_node(estado)
        
        G.add_edge('inicio', automata.estado_inicial)
        
        for (origen, simbolo), destinos in automata.transiciones.items():
            for destino in destinos:
                G.add_edge(origen, destino, key=f"{origen}-{simbolo}-{destino}", label=simbolo)
        
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        nx.draw_networkx_nodes(G, pos, nodelist=['inicio'], 
                              node_color='lightgray', node_size=600, node_shape='s')
        
        # Dibujar todos los estados con el mismo color
        nx.draw_networkx_nodes(G, pos, nodelist=automata.estados, 
                              node_color='lightgray', node_size=800)
        
        # Dibujar doble círculo para estados de aceptación
        ax = plt.gca()
        for estado in automata.estados_finales:
            if estado in pos:
                x, y = pos[estado]
                # Círculo exterior
                circle_outer = plt.Circle((x, y), 0.06, fill=False, color='black', linewidth=2)
                ax.add_patch(circle_outer)
                # Círculo interior ya está dibujado por networkx
        
        # NO dibujar aristas automáticamente para evitar conflictos
        # nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20)
        
        # Dibujar etiquetas de estados centradas
        labels = {estado: estado for estado in automata.estados}
        labels['inicio'] = 'inicio'
        nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold')
        
        # Dibujar aristas personalizadas para evitar solapamiento
        DiagramViewer._draw_custom_edges(automata, pos, plt.gca())
        
        # Dibujar arista de inicio manualmente
        ax = plt.gca()
        ax.annotate('', xy=pos[automata.estado_inicial], xytext=pos['inicio'],
                   arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
        
        plt.title(titulo, size=16)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def _draw_custom_edges(automata, pos, ax):
        """Dibuja transiciones con estética mejorada"""
        # Agrupar transiciones
        transitions_by_pair = {}
        self_loops = {}
        
        for (origen, simbolo), destinos in automata.transiciones.items():
            for destino in destinos:
                if origen == destino:
                    # Self-loop
                    if origen not in self_loops:
                        self_loops[origen] = []
                    self_loops[origen].append(simbolo)
                else:
                    # Transición normal
                    key = (origen, destino)
                    if key not in transitions_by_pair:
                        transitions_by_pair[key] = []
                    transitions_by_pair[key].append(simbolo)
        
        # Dibujar self-loops
        for estado, simbolos in self_loops.items():
            for i, simbolo in enumerate(simbolos):
                DiagramUtils.draw_self_loop(ax, pos, estado, simbolo, i)
        
        # Dibujar cada transición como línea independiente
        for (origen, destino), simbolos in transitions_by_pair.items():
            num_simbolos = len(simbolos)
            
            for i, simbolo in enumerate(simbolos):
                # SIEMPRE usar curvas separadas para cada transición
                if num_simbolos == 1:
                    curve_height = 0.15  # Curva ligera para transición única
                else:
                    curve_height = (i - num_simbolos/2 + 0.5) * 0.3  # Curvas separadas
                
                DiagramUtils.draw_curved_transition(
                    ax, pos[origen], pos[destino], simbolo, curve_height
                )
    
    @staticmethod
    def dibujar_diagrama_burbuja(afd, titulo):
        """Dibuja un diagrama de burbuja para el AFD"""
        import matplotlib.patches as patches
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Obtener estados y símbolos
        estados = list(afd.estados)
        simbolos = list(afd.alfabeto)
        
        # Verificar si hay transiciones a ERROR para agregarlo al diagrama
        tiene_error = False
        for (origen, simbolo), destino in afd.transiciones.items():
            if destino == "ERROR":
                tiene_error = True
                break
        
        # Agregar ERROR solo para el diagrama si es necesario
        if tiene_error and "ERROR" not in estados:
            estados.append("ERROR")
            print(f"DEBUG: Estado ERROR agregado al diagrama para visualización")
        
        # Recalcular posiciones en grid DESPUÉS de agregar ERROR
        cols = min(4, len(estados))  # Máximo 4 columnas
        rows = (len(estados) + cols - 1) // cols
        
        # Espaciado
        x_spacing = 3
        y_spacing = 2.5
        
        # Dibujar cada estado como burbuja
        print(f"DEBUG: Estados a dibujar: {estados}")
        for i, estado in enumerate(estados):
            row = i // cols
            col = i % cols
            
            x = col * x_spacing
            y = (rows - row - 1) * y_spacing  # Invertir Y para que vaya de arriba a abajo
            
            # Dibujar círculo principal (rojo para ERROR)
            color = 'lightcoral' if estado == "ERROR" else 'lightblue'
            circle = patches.Circle((x, y), 0.4, fill=True, facecolor=color, 
                                   edgecolor='navy', linewidth=2)
            ax.add_patch(circle)
            
            # Doble círculo para estados de aceptación
            if estado in afd.estados_finales:
                circle_outer = patches.Circle((x, y), 0.5, fill=False, 
                                            edgecolor='navy', linewidth=2)
                ax.add_patch(circle_outer)
            
            # Etiqueta del estado
            estado_nombre = DiagramViewer._format_estado_burbuja(estado)
            ax.text(x, y, estado_nombre, ha='center', va='center', 
                   fontsize=9, fontweight='bold')
            
            # Dibujar transiciones como flechas
            for simbolo in simbolos:
                destino = afd.transiciones.get((estado, simbolo))
                
                if destino and destino in estados:
                    destino_idx = estados.index(destino)
                    dest_row = destino_idx // cols
                    dest_col = destino_idx % cols
                    dest_x = dest_col * x_spacing
                    dest_y = (rows - dest_row - 1) * y_spacing
                    
                    # Dibujar flecha
                    if estado != destino:  # No self-loop
                        DiagramViewer._draw_bubble_arrow(ax, x, y, dest_x, dest_y, simbolo)
                    else:  # Self-loop
                        DiagramViewer._draw_bubble_self_loop(ax, x, y, simbolo)
        
        ax.set_xlim(-1, cols * x_spacing)
        ax.set_ylim(-1, rows * y_spacing)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.title(titulo, size=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def _format_estado_burbuja(estado):
        """Formatea el nombre del estado para el diagrama de burbuja"""
        if isinstance(estado, frozenset):
            return ''.join(sorted(estado)) if estado else "∅"
        return str(estado)
    
    @staticmethod
    def _draw_bubble_arrow(ax, x1, y1, x2, y2, simbolo):
        """Dibuja una flecha entre burbujas"""
        # Calcular puntos en el borde de los círculos
        import numpy as np
        dx = x2 - x1
        dy = y2 - y1
        dist = np.sqrt(dx**2 + dy**2)
        
        if dist > 0:
            # Normalizar
            dx_norm = dx / dist
            dy_norm = dy / dist
            
            # Puntos de inicio y fin en los bordes
            start_x = x1 + 0.4 * dx_norm
            start_y = y1 + 0.4 * dy_norm
            end_x = x2 - 0.4 * dx_norm
            end_y = y2 - 0.4 * dy_norm
            
            # Dibujar flecha
            ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                       arrowprops=dict(arrowstyle='->', color='darkblue', lw=2))
            
            # Etiqueta en el medio
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2 + 0.15
            ax.text(mid_x, mid_y, simbolo, ha='center', va='center', fontsize=10,
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.8))
    
    @staticmethod
    def _draw_bubble_self_loop(ax, x, y, simbolo):
        """Dibuja un self-loop en una burbuja"""
        import matplotlib.patches as patches
        
        # Círculo pequeño arriba del estado
        loop_circle = patches.Circle((x, y + 0.7), 0.15, fill=False, 
                                   edgecolor='darkblue', linewidth=2)
        ax.add_patch(loop_circle)
        
        # Flecha
        ax.annotate('', xy=(x + 0.1, y + 0.6), xytext=(x - 0.1, y + 0.6),
                   arrowprops=dict(arrowstyle='->', color='darkblue', lw=2))
        
        # Etiqueta
        ax.text(x, y + 0.9, simbolo, ha='center', va='center', fontsize=10,
               bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.8))
    
    @staticmethod
    def dibujar_diagrama_afd(afd, titulo):
        G = nx.DiGraph()
        G.add_node('inicio')
        
        estado_labels = {}
        for i, estado in enumerate(sorted(afd.estados, key=str)):
            if isinstance(estado, frozenset):
                contenido = ''.join(sorted(estado))
                estado_labels[estado] = f"q{i}\n{{{contenido}}}"
            else:
                estado_labels[estado] = str(estado)
        
        for estado in afd.estados:
            G.add_node(estado)
        
        G.add_edge('inicio', afd.estado_inicial)
        
        for (origen, simbolo), destino in afd.transiciones.items():
            G.add_edge(origen, destino, key=f"{origen}-{simbolo}-{destino}", label=simbolo)
        
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        nx.draw_networkx_nodes(G, pos, nodelist=['inicio'], 
                              node_color='lightgray', node_size=600, node_shape='s')
        
        # Dibujar todos los estados con el mismo color
        nx.draw_networkx_nodes(G, pos, nodelist=afd.estados, 
                              node_color='lightgray', node_size=1200)
        
        # Dibujar doble círculo para estados de aceptación
        ax = plt.gca()
        for estado in afd.estados_finales:
            if estado in pos:
                x, y = pos[estado]
                # Círculo exterior
                circle_outer = plt.Circle((x, y), 0.08, fill=False, color='black', linewidth=2)
                ax.add_patch(circle_outer)
                # Círculo interior ya está dibujado por networkx
        
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20, width=1.5)
        
        # Dibujar etiquetas de estados centradas
        labels = estado_labels.copy()
        labels['inicio'] = 'inicio'
        nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
        
        # Crear etiquetas para cada arista individual en AFD con mejor estilo
        edge_labels = {}
        for u, v, data in G.edges(data=True):
            if 'label' in data:
                edge_labels[(u, v)] = data['label']
        
        # Dibujar etiquetas de aristas con estilo mejorado
        for (u, v), label in edge_labels.items():
            mid_x = (pos[u][0] + pos[v][0]) / 2
            mid_y = (pos[u][1] + pos[v][1]) / 2 + 0.12
            plt.text(mid_x, mid_y, label, fontsize=11, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.9, edgecolor='navy'))
        
        plt.title(titulo, size=16)
        plt.axis('off')
        plt.show()