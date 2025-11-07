# Convertidor AFND a AFD

Implementación en Python para convertir Autómatas Finitos No Determinísticos (AFND) en Autómatas Finitos Determinísticos (AFD) con interfaz gráfica usando el algoritmo de construcción de subconjuntos.

## 🚀 Instalación y Ejecución

### Opción 1: Ejecutable (Recomendado)
```bash
# Ejecutar directamente sin instalación
dist/Convertidor_AFND_AFD.exe
```

### Opción 2: Desde código fuente
```bash
# Instalar dependencias
pip install --index-url https://pypi.org/simple/ -r requirements.txt

# Ejecutar aplicación
python main.py
```

### Opción 3: Crear nuevo ejecutable
```bash
# Instalar PyInstaller y crear ejecutable
pip install --index-url https://pypi.org/simple/ pyinstaller
python -m PyInstaller --onefile --windowed --name "Convertidor_AFND_AFD" main.py
```

## 📋 Dependencias

- **matplotlib>=3.5.0**: Visualización de diagramas
- **networkx>=2.8.0**: Grafos y algoritmos de red  
- **numpy>=1.21.0**: Operaciones matemáticas
- **tkinter**: Interfaz gráfica (incluido en Python)
- **pyinstaller>=5.0.0**: Creación de ejecutables

## 📝 Manual de Usuario - Formato de Entrada

### PARTE 1: DATOS BÁSICOS

#### 🔤 Estados
- **Formato**: Letras mayúsculas separadas por comas
- **Permitido**: `A,B,C,D` o `Q0,Q1,Q2`
- **Restricciones**: 
  - Solo letras (A-Z)
  - Una letra por estado
  - Separados por comas
  - Conversión automática a mayúsculas
- **Ejemplos válidos**: `A,B,C`, `Q,R,S,T`
- **Ejemplos inválidos**: `a,b` (minúsculas), `AB,CD` (múltiples letras), `A B C` (espacios)

#### 🔢 Símbolos de Entrada
- **Formato**: Exactamente 2 números separados por coma
- **Permitido**: `0,1` o `1000,2000`
- **Restricciones**:
  - Solo números (0-9)
  - Exactamente 2 símbolos
  - Separados por una coma
  - Sin espacios adicionales
- **Ejemplos válidos**: `0,1`, `10,20`, `100,200`
- **Ejemplos inválidos**: `0,1,2` (3 símbolos), `a,b` (letras), `0 1` (sin coma)

#### 🎯 Estado Inicial
- **Formato**: Una sola letra mayúscula
- **Permitido**: `A` o `Q`
- **Restricciones**:
  - Debe existir en la lista de estados
  - Solo una letra
  - Conversión automática a mayúsculas
- **Ejemplos válidos**: `A`, `B`, `Q`
- **Ejemplos inválidos**: `AB` (múltiples letras), `A,B` (con coma), `1` (número)

#### ✅ Estados de Aceptación
- **Formato**: Letras mayúsculas separadas por comas
- **Permitido**: `B,C` o `Q,R`
- **Restricciones**:
  - Deben existir en la lista de estados
  - Separados por comas
  - Conversión automática a mayúsculas
- **Ejemplos válidos**: `B`, `B,C`, `Q,R,S`
- **Ejemplos inválidos**: `X` (no existe), `B C` (sin coma)

### PARTE 2: MATRIZ DE TRANSICIONES

#### 🔄 Transiciones
- **Formato**: Se genera automáticamente una matriz basada en estados y símbolos
- **Entrada por celda**: Estados destino separados por comas
- **Permitido**: `B`, `B,C` (no determinístico), vacío (sin transición)
- **Restricciones**:
  - Solo estados que existen
  - Conversión automática a mayúsculas
  - Múltiples destinos separados por comas
- **Ejemplos válidos**: `B`, `B,C`, `` (vacío)
- **Ejemplos inválidos**: `X` (estado inexistente), `B;C` (separador incorrecto)

#### 📊 Columna Acepta/Rechaza
- **Formato**: Solo lectura, se llena automáticamente
- **Valores**: `1` (acepta) o `0` (rechaza)
- **Lógica**: `1` si el estado está en estados de aceptación, `0` si no

## 🔄 Flujo de Trabajo Completo

### Paso 1: Datos Básicos
1. Llenar **Estados** (ej: `A,B,C,D`)
2. Llenar **Símbolos** (ej: `0,1`)
3. Llenar **Estado inicial** (ej: `A`)
4. Llenar **Estados finales** (ej: `C,D`)
5. Hacer clic en **"Validar Datos Básicos"**
6. ✅ Si es válido, se habilita la Parte 2

### Paso 2: Transiciones
1. Se genera automáticamente la **matriz de transiciones**
2. Llenar cada celda con estados destino
3. Hacer clic en **"Validar AFND"**
4. ✅ Sistema detecta si es determinístico o no
5. Se habilitan botones de visualización

### Paso 3: Conversión y Visualización
1. **"Mostrar AFND"**: Visualiza el autómata original
2. **"Convertir a AFD"**: Aplica algoritmo de construcción de subconjuntos
   - Solicita secuencia de prueba
   - Genera tabla de conversión
3. **"Mostrar AFD"**: Visualiza el autómata convertido en diagrama de burbuja

## 🎨 Características de Visualización

### Diagrama AFND Original
- **Estados normales**: Círculos grises
- **Estados de aceptación**: Doble círculo
- **Transiciones**: Flechas curvas con etiquetas
- **Self-loops**: Bucles superiores
- **Nodo inicio**: Cuadrado gris

### Diagrama AFD (Burbuja)
- **Estados AFD**: Burbujas azules con nombres de subconjuntos
- **Estados de aceptación**: Doble círculo
- **Estado ERROR**: Burbuja roja (si existe)
- **Transiciones**: Flechas azules con etiquetas amarillas
- **Self-loops**: Círculos superiores

## 🏗️ Arquitectura del Código

```
automata/
├── main.py                           # Punto de entrada (MVC setup)
├── src/
│   ├── config/
│   │   └── constants.py             # Constantes de la aplicación
│   ├── models/
│   │   ├── automata.py              # Clases AFND y AFD + algoritmo conversión
│   │   └── validator.py             # Validaciones de entrada
│   ├── views/
│   │   ├── main_window.py           # Interfaz gráfica principal
│   │   └── diagram_viewer.py        # Visualizador de diagramas
│   ├── controllers/
│   │   └── automata_controller.py   # Lógica de control MVC
│   └── utils/
│       ├── diagram_utils.py         # Utilidades de diagramas
│       ├── error_handler.py         # Manejo centralizado de errores
│       ├── input_validators.py      # Validadores en tiempo real
│       ├── ui_helpers.py            # Helpers de interfaz
│       └── ui_optimizer.py          # Optimizaciones de UI
├── dist/
│   └── Convertidor_AFND_AFD.exe     # Ejecutable final
├── requirements.txt                  # Dependencias Python
└── README.md                        # Esta documentación
```

## 🧮 Algoritmo de Conversión

### Construcción de Subconjuntos
1. **Estado inicial AFD**: `{estado_inicial_AFND}`
2. **Para cada estado AFD**:
   - Para cada símbolo del alfabeto
   - Calcular unión de transiciones de todos los estados del subconjunto
   - Si el resultado es nuevo, agregarlo como estado AFD
3. **Estados de aceptación AFD**: Subconjuntos que contienen al menos un estado de aceptación del AFND
4. **Transiciones ERROR**: Si no hay transición, va a estado ERROR

### Ejemplo de Conversión
```
AFND: A --0--> {B,C}, A --1--> {B}
AFD:  {A} --0--> {B,C}, {A} --1--> {B}
      {B,C} --0--> ..., {B,C} --1--> ...
```

## ⚠️ Validaciones y Restricciones

### Validaciones en Tiempo Real
- **Estados**: Solo letras y comas
- **Símbolos**: Solo números y máximo 1 coma
- **Estado inicial**: Solo 1 letra
- **Estados finales**: Solo letras y comas
- **Matriz**: Solo letras y comas por celda

### Validaciones de Consistencia
- Estado inicial debe existir en estados
- Estados finales deben existir en estados
- Estados en transiciones deben existir
- Símbolos en transiciones deben existir
- Exactamente 2 símbolos de entrada

### Manejo de Errores
- Logging automático en `automata_errors.log`
- Mensajes de error descriptivos
- Validación progresiva (Parte 1 → Parte 2)
- Reset completo disponible

## 🎯 Casos de Uso Típicos

### Ejemplo 1: AFND Simple
```
Estados: A,B,C
Símbolos: 0,1
Inicial: A
Finales: C

Transiciones:
A + 0 → B
A + 1 → B,C  (No determinístico)
B + 0 → C
B + 1 → ∅
C + 0 → ∅
C + 1 → ∅
```

### Ejemplo 2: AFD Resultante
```
Estados AFD: {A}, {B}, {B,C}, ERROR
Transiciones:
{A} + 0 → {B}
{A} + 1 → {B,C}
{B} + 0 → {C}
{B} + 1 → ERROR
{B,C} + 0 → {C}
{B,C} + 1 → ERROR
```

## 🔧 Solución de Problemas

### Error: "Estado no existe"
- Verificar que todos los estados estén en la lista inicial
- Revisar mayúsculas/minúsculas

### Error: "Símbolo no existe"
- Verificar que solo uses los 2 símbolos definidos
- Revisar espacios extra

### Error: "Formato incorrecto"
- Revisar separadores (comas, no espacios)
- Verificar que no haya caracteres especiales

### Aplicación no responde
- Reiniciar con botón "Limpiar Datos"
- Verificar logs en `automata_errors.log`