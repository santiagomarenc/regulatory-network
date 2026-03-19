
# Casos de prueba

Este documento define los casos de prueba del ejercicio antes de la implementación. Su propósito es dejar explícito qué entradas debe aceptar el programa y qué salidas se esperan, tanto para la versión básica como para la versión extendida.

## Convenciones

Cada interacción se representa como una tupla con la forma:

`(TF, gene, effect)`

donde:

- `TF` es el factor de transcripción
- `gene` es el gen regulado
- `effect` es el tipo de regulación:
  - `+` para activación
  - `-` para represión

Las salidas esperadas asumen que:

- los TF se reportan en orden alfabético
- la lista de genes de cada TF también se reporta en orden alfabético

---

## Caso 1: un TF con regulación mixta

### Entrada

```python
interactions = [
    ("AraC", "araA", "+"),
    ("AraC", "araB", "-"),
]
```

### Salida esperada, versión 1

| TF   | Total | Genes      |
| ---- | ----- | ---------- |
| AraC | 2     | araA, araB |

### Salida esperada, versión 2

| TF   | Total | Activados | Reprimidos | Tipo |
| ---- | ----- | --------- | ---------- | ---- |
| AraC | 2     | 1         | 1          | dual |

### Qué valida

* agrupación de varios genes bajo un mismo TF
* conteo correcto del total de genes
* clasificación correcta como `dual`

---

## Caso 2: dos TF independientes

### Entrada

```python
interactions = [
    ("AraC", "araA", "+"),
    ("LexA", "recA", "-"),
]
```

### Salida esperada, versión 1

| TF   | Total | Genes |
| ---- | ----- | ----- |
| AraC | 1     | araA  |
| LexA | 1     | recA  |

### Salida esperada, versión 2

| TF   | Total | Activados | Reprimidos | Tipo      |
| ---- | ----- | --------- | ---------- | --------- |
| AraC | 1     | 1         | 0          | activador |
| LexA | 1     | 0         | 1          | represor  |

### Qué valida

* manejo de múltiples TF
* separación correcta de interacciones por TF
* clasificación correcta para activador y represor

---

## Caso 3: un TF solo activador

### Entrada

```python
interactions = [
    ("CRP", "lacZ", "+"),
    ("CRP", "lacY", "+"),
    ("CRP", "lacA", "+"),
]
```

### Salida esperada, versión 1

| TF  | Total | Genes            |
| --- | ----- | ---------------- |
| CRP | 3     | lacA, lacY, lacZ |

### Salida esperada, versión 2

| TF  | Total | Activados | Reprimidos | Tipo      |
| --- | ----- | --------- | ---------- | --------- |
| CRP | 3     | 3         | 0          | activador |

### Qué valida

* acumulación de varios genes para un mismo TF
* ordenamiento alfabético de genes
* clasificación correcta como `activador`

---

## Caso 4: múltiples TF mezclados

### Entrada

```python
interactions = [
    ("AraC", "araA", "+"),
    ("AraC", "araB", "-"),
    ("CRP", "lacZ", "+"),
    ("LexA", "recA", "-"),
]
```

### Salida esperada, versión 1

| TF   | Total | Genes      |
| ---- | ----- | ---------- |
| AraC | 2     | araA, araB |
| CRP  | 1     | lacZ       |
| LexA | 1     | recA       |

### Salida esperada, versión 2

| TF   | Total | Activados | Reprimidos | Tipo      |
| ---- | ----- | --------- | ---------- | --------- |
| AraC | 2     | 1         | 1          | dual      |
| CRP  | 1     | 1         | 0          | activador |
| LexA | 1     | 0         | 1          | represor  |

### Qué valida

* agrupación correcta con varios TF en una misma colección
* ordenamiento de TF en la salida
* coexistencia de los tres tipos regulatorios

---