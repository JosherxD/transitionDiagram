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
        
        estados_normales = automata.estados - automata.estados_finales
        nx.draw_networkx_nodes(G, pos, nodelist=estados_normales, 
                              node_color='lightgray', node_size=800)
        
        nx.draw_networkx_nodes(G, pos, nodelist=automata.estados_finales, 
                              node_color='lightgreen', node_size=800)
        
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
    def dibujar_diagrama_afd(afd, titulo):
        G = nx.DiGraph()
        G.add_node('inicio')
        
        estado_labels = {}
        for i, estado in enumerate(sorted(afd.estados, key=str)):
            if isinstance(estado, frozenset):
                contenido = ','.join(sorted(estado))
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
        
        estados_normales = afd.estados - afd.estados_finales
        nx.draw_networkx_nodes(G, pos, nodelist=estados_normales, 
                              node_color='lightgray', node_size=1200)
        
        nx.draw_networkx_nodes(G, pos, nodelist=afd.estados_finales, 
                              node_color='lightgreen', node_size=1200)
        
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