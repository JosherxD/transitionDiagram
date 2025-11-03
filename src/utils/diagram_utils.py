# diagram_utils.py - Utilidades para visualización estética de diagramas
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class DiagramUtils:
    @staticmethod
    def draw_self_loop(ax, pos, state, label, angle_offset=0):
        """Dibuja un bucle que sale y regresa al mismo estado"""
        x, y = pos[state]
        angle = 90 + angle_offset * 45  # Ángulo base hacia arriba
        
        # Puntos de salida y llegada en el borde del círculo del estado
        node_radius = 0.15  # Radio del nodo del estado
        start_angle = angle - 20
        end_angle = angle + 20
        
        start_x = x + node_radius * np.cos(np.radians(start_angle))
        start_y = y + node_radius * np.sin(np.radians(start_angle))
        end_x = x + node_radius * np.cos(np.radians(end_angle))
        end_y = y + node_radius * np.sin(np.radians(end_angle))
        
        # Punto de control para crear el arco
        control_distance = 0.4
        control_x = x + control_distance * np.cos(np.radians(angle))
        control_y = y + control_distance * np.sin(np.radians(angle))
        
        # Dibujar arco bezier
        t = np.linspace(0, 1, 100)
        arc_x = (1-t)**2 * start_x + 2*(1-t)*t * control_x + t**2 * end_x
        arc_y = (1-t)**2 * start_y + 2*(1-t)*t * control_y + t**2 * end_y
        
        ax.plot(arc_x, arc_y, color='gray', linewidth=1.5)
        
        # Flecha al final del arco
        arrow_t = 0.9
        arrow_x = (1-arrow_t)**2 * start_x + 2*(1-arrow_t)*arrow_t * control_x + arrow_t**2 * end_x
        arrow_y = (1-arrow_t)**2 * start_y + 2*(1-arrow_t)*arrow_t * control_y + arrow_t**2 * end_y
        
        ax.annotate('', xy=(end_x, end_y), xytext=(arrow_x, arrow_y),
                   arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
        
        # Etiqueta en el punto más alto del arco
        ax.text(control_x, control_y - 0.05, label, fontsize=10, ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9))
    
    @staticmethod
    def draw_curved_transition(ax, start_pos, end_pos, label, curve_height=0.3):
        """Dibuja una transición curvada entre dos estados"""
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Punto medio
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Vector perpendicular para la curva
        dx = x2 - x1
        dy = y2 - y1
        length = np.sqrt(dx**2 + dy**2)
        
        if length > 0:
            perp_x = -dy / length
            perp_y = dx / length
        else:
            perp_x, perp_y = 0, 1
        
        # Punto de control para la curva
        control_x = mid_x + perp_x * curve_height
        control_y = mid_y + perp_y * curve_height
        
        # Dibujar curva bezier
        t = np.linspace(0, 1, 100)
        curve_x = (1-t)**2 * x1 + 2*(1-t)*t * control_x + t**2 * x2
        curve_y = (1-t)**2 * y1 + 2*(1-t)*t * control_y + t**2 * y2
        
        ax.plot(curve_x, curve_y, color='gray', linewidth=1.5)
        
        # Flecha al final
        arrow_t = 0.85
        arrow_x = (1-arrow_t)**2 * x1 + 2*(1-arrow_t)*arrow_t * control_x + arrow_t**2 * x2
        arrow_y = (1-arrow_t)**2 * y1 + 2*(1-arrow_t)*arrow_t * control_y + arrow_t**2 * y2
        
        end_t = 0.95
        end_x = (1-end_t)**2 * x1 + 2*(1-end_t)*end_t * control_x + end_t**2 * x2
        end_y = (1-end_t)**2 * y1 + 2*(1-end_t)*end_t * control_y + end_t**2 * y2
        
        ax.annotate('', xy=(end_x, end_y), xytext=(arrow_x, arrow_y),
                   arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
        
        # Etiqueta en el punto más alto de la curva
        label_x = control_x
        label_y = control_y + 0.1
        ax.text(label_x, label_y, label, fontsize=10, ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9))