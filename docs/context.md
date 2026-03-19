# Contexto

Este ejercicio está inspirado en un problema básico de regulación genética. En biología molecular, los factores de transcripción (TF, por sus siglas en inglés) son proteínas que regulan la expresión de genes. Esa regulación puede ocurrir de dos formas principales:

- **activación (`+`)**: el TF favorece la expresión del gen
- **represión (`-`)**: el TF reduce o bloquea la expresión del gen

Para este ejercicio, cada interacción regulatoria se representa como una fila con tres campos:

`TF  Gene  Effect`

Por ejemplo:

    AraC araA +
    AraC araB -
    LexA recA -
    CRP lacZ +
    CRP lacY +

Aquí:

- `TF` es el regulador o factor de transcripción
- `Gene` es el gen regulado
- `Effect` indica el tipo de efecto regulatorio:
  - `+` = activación
  - `-` = represión

## Propósito del ejercicio

A partir de una colección de interacciones regulatorias, el programa debe construir un resumen por factor de transcripción. En una primera versión, el resumen debe indicar:

- el nombre del TF
- el número total de genes regulados
- la lista de genes regulados

Ejemplo de salida conceptual:

| TF   | Total de genes regulados | Lista de genes |
|------|---------------------------|----------------|
| AraC | 2                         | araA, araB     |
| LexA | 1                         | recA           |
| CRP  | 2                         | lacZ, lacY     |

En una segunda versión, el programa debe extender ese análisis para clasificar cada TF según su comportamiento regulatorio:

- **activador**: solo presenta interacciones `+`
- **represor**: solo presenta interacciones `-`
- **dual**: presenta interacciones `+` y `-`

## Enfoque computacional

Este problema es útil como ejercicio porque obliga a transformar una colección de filas de texto en estructuras de datos con relaciones explícitas entre elementos. En particular, interesa modelar relaciones del tipo:

`TF -> genes regulados`

y posteriormente:

`TF -> genes regulados + tipo de regulación`

Para resolverlo en Python se utilizarán principalmente:

- **tuplas**, para representar una interacción individual
- **listas**, para almacenar colecciones de interacciones o genes
- **diccionarios**, para asociar cada TF con sus genes y resumir la información

## Alcance

Este ejercicio no busca modelar una red de regulación biológica real con toda su complejidad. Solo pretende resolver un problema acotado de organización y resumen de datos regulatorios.

No se consideran, por ahora:

- condiciones experimentales
- intensidad de regulación
- evidencia biológica
- regulación indirecta
- interacciones temporales o contextuales

El objetivo es desarrollar un programa claro, correcto y fácil de extender, aplicando estructuras de datos, iteración y buenas prácticas básicas de organización del código.