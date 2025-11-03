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
        """Dibuja aristas personalizadas para evitar solapamiento"""
        # Contar aristas entre cada par de nodos
        edge_counts = DiagramUtils.count_edges_between_nodes(automata.transiciones)
        edge_indices = {}
        
        for (origen, simbolo), destinos in automata.transiciones.items():
            for destino in destinos:
                key = (origen, destino)
                if key not in edge_indices:
                    edge_indices[key] = 0
                
                edge_count = edge_counts[key]
                edge_index = edge_indices[key]
                
                if edge_count > 1:
                    # Usar arista curvada para múltiples conexiones
                    control_point = DiagramUtils.calculate_curved_edge_positions(
                        pos, origen, destino, edge_count, edge_index
                    )
                    if control_point:
                        DiagramUtils.draw_curved_arrow(
                            ax, pos[origen], pos[destino], control_point, simbolo
                        )
                    else:
                        # Fallback a línea recta
                        ax.annotate('', xy=pos[destino], xytext=pos[origen],
                                   arrowprops=dict(arrowstyle='->', color='gray'))
                        # Agregar etiqueta más arriba
                        mid_x = (pos[origen][0] + pos[destino][0]) / 2
                        mid_y = (pos[origen][1] + pos[destino][1]) / 2 + 0.15
                        ax.text(mid_x, mid_y, simbolo, fontsize=11, ha='center', va='center',
                               bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.9, edgecolor='navy'))
                else:
                    # Usar línea recta para conexión única
                    ax.annotate('', xy=pos[destino], xytext=pos[origen],
                               arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
                    # Agregar etiqueta más arriba
                    mid_x = (pos[origen][0] + pos[destino][0]) / 2
                    mid_y = (pos[origen][1] + pos[destino][1]) / 2 + 0.15
                    ax.text(mid_x, mid_y, simbolo, fontsize=11, ha='center', va='center',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.9, edgecolor='navy'))
                
                edge_indices[key] += 1
    
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