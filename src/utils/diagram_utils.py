# diagram_utils.py - Utilidades para mejorar la visualización de diagramas
import matplotlib.pyplot as plt
import numpy as np

class DiagramUtils:
    @staticmethod
    def calculate_curved_edge_positions(pos, u, v, edge_count, edge_index):
        """Calcula posiciones para aristas curvadas cuando hay múltiples conexiones"""
        if edge_count == 1:
            return None  # Usar línea recta
        
        # Calcular punto medio
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Calcular vector perpendicular
        dx = x2 - x1
        dy = y2 - y1
        length = np.sqrt(dx**2 + dy**2)
        
        if length == 0:
            return None
        
        # Vector perpendicular normalizado
        perp_x = -dy / length
        perp_y = dx / length
        
        # Desplazamiento basado en el índice de la arista
        offset = (edge_index - edge_count/2 + 0.5) * 0.3
        
        # Punto de control para la curva
        control_x = mid_x + perp_x * offset
        control_y = mid_y + perp_y * offset
        
        return (control_x, control_y)
    
    @staticmethod
    def draw_curved_arrow(ax, start, end, control, label, color='gray'):
        """Dibuja una flecha curvada con etiqueta"""
        # Crear curva bezier cuadrática
        t = np.linspace(0, 1, 100)
        x = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 * end[0]
        y = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 * end[1]
        
        # Dibujar curva
        ax.plot(x, y, color=color, linewidth=1)
        
        # Dibujar punta de flecha
        arrow_pos = 0.9  # Posición de la flecha en la curva
        arrow_x = (1-arrow_pos)**2 * start[0] + 2*(1-arrow_pos)*arrow_pos * control[0] + arrow_pos**2 * end[0]
        arrow_y = (1-arrow_pos)**2 * start[1] + 2*(1-arrow_pos)*arrow_pos * control[1] + arrow_pos**2 * end[1]
        
        # Calcular dirección de la flecha
        next_pos = 0.95
        next_x = (1-next_pos)**2 * start[0] + 2*(1-next_pos)*next_pos * control[0] + next_pos**2 * end[0]
        next_y = (1-next_pos)**2 * start[1] + 2*(1-next_pos)*next_pos * control[1] + next_pos**2 * end[1]
        
        dx = next_x - arrow_x
        dy = next_y - arrow_y
        
        ax.annotate('', xy=(next_x, next_y), xytext=(arrow_x, arrow_y),
                   arrowprops=dict(arrowstyle='->', color=color, lw=1))
        
        # Posición de la etiqueta en el punto medio de la curva
        label_pos = 0.5
        label_x = (1-label_pos)**2 * start[0] + 2*(1-label_pos)*label_pos * control[0] + label_pos**2 * end[0]
        label_y = (1-label_pos)**2 * start[1] + 2*(1-label_pos)*label_pos * control[1] + label_pos**2 * end[1] + 0.25
        
        # Agregar etiqueta con mejor estilo
        ax.text(label_x, label_y, label, fontsize=11, ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.9, edgecolor='navy'))
    
    @staticmethod
    def count_edges_between_nodes(transitions):
        """Cuenta las aristas entre cada par de nodos"""
        edge_counts = {}
        for (origen, simbolo), destinos in transitions.items():
            for destino in destinos:
                key = (origen, destino)
                if key not in edge_counts:
                    edge_counts[key] = 0
                edge_counts[key] += 1
        return edge_counts