Bien. Esa decisión debe quedar explícita en `docs/design.md`, no solo mencionada al pasar, porque afecta el comportamiento del programa y las pruebas.

Pega esto en `docs/design.md`:

````markdown
# Diseño

## Descripción del problema

El programa debe analizar una colección de interacciones regulatorias entre factores de transcripción (TF) y genes. Cada interacción tiene tres componentes:

`TF  gene  effect`

donde:

- `TF` es el factor de transcripción
- `gene` es el gen regulado
- `effect` es el tipo de regulación:
  - `+` para activación
  - `-` para represión

A partir de esa colección, el programa debe generar dos tipos de resumen:

1. **Versión 1**: resumen por TF con:
   - total de genes regulados
   - lista de genes regulados

2. **Versión 2**: extensión del análisis para incluir:
   - total de genes regulados
   - número de genes activados
   - número de genes reprimidos
   - tipo regulatorio del TF: `activador`, `represor` o `dual`

---

## Modelo de datos

Para este ejercicio se usarán tres estructuras principales:

### 1. Tuplas

Cada interacción individual se representará como una tupla:

```python
("AraC", "araA", "+")
````

Se eligen tuplas porque una interacción es un registro fijo de tres elementos relacionados.

### 2. Listas

La colección completa de interacciones se representará como una lista de tuplas:

```python
interactions = [
    ("AraC", "araA", "+"),
    ("AraC", "araB", "-"),
    ("LexA", "recA", "-"),
]
```

Las listas permiten recorrer secuencialmente todas las interacciones de entrada.

### 3. Diccionarios

El resumen por TF se construirá usando diccionarios, porque el problema requiere asociar cada TF con información acumulada.

Conceptualmente:

```text
TF -> genes regulados
```

y en la versión extendida:

```text
TF -> genes regulados + conteos por tipo de efecto
```

---

