<<<<<<< HEAD
# Convertidor AFND a AFD

Implementación en Python para convertir Autómatas Finitos No Determinísticos (AFND) en Autómatas Finitos Determinísticos (AFD).

## Características

- ✅ Validación de autómatas no determinísticos
- 🔄 Conversión usando algoritmo de construcción de subconjuntos
- 📊 Visualización gráfica de diagramas de burbuja
- 🎯 Soporte para transiciones épsilon (ε)
- 💻 Interfaz de consola interactiva

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Modo Interactivo
```bash
python main.py
```

### Ejemplo Predefinido
```bash
python ejemplo_uso.py
```

## Formato de Entrada

### Estados
Letras A-Z separadas por comas: `A,B,C`

### Símbolos de entrada
Sólo 0 y 1: `0,1,ε`

### Transiciones
Formato: `estado_origen,simbolo,estado_destino`
Múltiples destinos: `A,0,B;C`

## Ejemplo de AFND

```
Estados: A,B,C
Símbolos: 0,1
Estado inicial: A
Estados de aceptación: C
Transiciones:
- A,0,A
- A,1,A
- A,0,B
- B,1,C
```

## Algoritmo

1. **Validación**: Detecta transiciones múltiples
2. **Epsilon-clausura**: Calcula estados alcanzables por ε
3. **Construcción de subconjuntos**: Genera estados del AFD
4. **Visualización**: Dibuja diagramas con NetworkX

## Colores del Diagrama

- ⬜ **Gris**: Estados normales y nodo inicio
- 🟢 **Verde**: Estados de aceptación
=======
# transitionDiagram
Código que te permite crear por medio de unos parámetros de entrada la validación y generación en imagen de un diagrama de transición
>>>>>>> develop
