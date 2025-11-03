# Convertidor AFND a AFD

Implementación en Python para convertir Autómatas Finitos No Determinísticos (AFND) en Autómatas Finitos Determinísticos (AFD) con interfaz gráfica.

## 🚀 Instalación

### Opción 1: Instalación automática (Windows)
```bash
install_dependencies.bat
```

### Opción 2: Instalación manual
```bash
pip install -r requirements.txt
```

## 📋 Dependencias

- **matplotlib**: Visualización de diagramas
- **networkx**: Grafos y algoritmos de red
- **numpy**: Operaciones matemáticas
- **tkinter**: Interfaz gráfica (incluido en Python)

## 🎯 Uso

```bash
python main.py
```

## 📝 Formato de entrada

### Parte 1: Datos básicos
- **Estados**: Letras mayúsculas separadas por comas (`A,B,C,D`)
- **Símbolos**: Exactamente 2 números separados por coma (`0,1` o `1000,2000`)
- **Estado inicial**: Una sola letra (`A`)
- **Estados finales**: Letras separadas por comas (`B,C`)

### Parte 2: Transiciones
- **Formato**: `origen,simbolo,destino`
- **Múltiples destinos**: `A,0,B;C`
- **Una transición por línea**

## ✨ Características

- ✅ **Validación en tiempo real** de entrada
- ✅ **Conversión automática** a mayúsculas
- ✅ **Interfaz progresiva** en 2 partes
- ✅ **Detección de no determinismo**
- ✅ **Visualización gráfica** de diagramas
- ✅ **Algoritmo de construcción** de subconjuntos

## 🏗️ Arquitectura

```
automata/
├── main.py                    # Punto de entrada
├── src/
│   ├── models/               # Lógica de negocio
│   │   ├── automata.py      # Clases AFND y AFD
│   │   └── validator.py     # Validaciones
│   ├── views/               # Interfaz gráfica
│   │   ├── main_window.py   # Ventana principal
│   │   └── diagram_viewer.py # Visualizador
│   └── controllers/         # Controladores
│       └── automata_controller.py
├── requirements.txt          # Dependencias
└── README.md                # Documentación
```

## 🔄 Flujo de trabajo

1. **Llenar datos básicos** (Estados, símbolos, etc.)
2. **Validar datos básicos** ✓
3. **Ingresar transiciones** (se habilita automáticamente)
4. **Validar AFND** ✓
5. **Convertir a AFD** ✓
6. **Visualizar diagramas** 📊

## 🎨 Colores del diagrama

- **Gris**: Estados normales y nodo inicio
- **Verde**: Estados de aceptación
- **Flechas grises**: Transiciones