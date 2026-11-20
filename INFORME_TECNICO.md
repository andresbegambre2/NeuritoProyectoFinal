# Informe técnico del NeuroEcosistema

**Universidad Santo Tomás, seccional Tunja · Electiva de Inteligencia Artificial**  
**Proyecto:** simulación de depredadores y presas  
**Fecha de generación de evidencia:** 20 de noviembre de 2026
Se implementó la simulación y se evaluó con 360 episodios reproducibles. Las redes aprendieron a imitar la regla experta, pero la política aleatoria mantuvo más presas vivas en los tres escenarios. Por tanto, los datos no respaldan que la política neuronal mejore la supervivencia; el informe explica este resultado y sus límites.

## 1 Problema y objetivo

Se implementó una simulación 2D donde presas buscan alimento y evitan depredadores, mientras los depredadores persiguen presas y recuperan energía al capturarlas. La pregunta experimental es si agentes con redes neuronales obtienen mejor desempeño que políticas sin aprendizaje en escenarios con recursos suficientes, escasez y presión de depredación/obstáculos.

## 2 Diseño e implementación

El mundo es una cuadrícula de 24×24 con 12 presas iniciales. Los escenarios son: abundancia (22 alimentos, 2 depredadores, sin obstáculos), escasez (7 alimentos, 2 depredadores), y presión (16 alimentos, 5 depredadores y 18 obstáculos). El alimento puede regenerarse. La energía se consume por paso y se recupera al comer o capturar.

Cada especie tiene una red neuronal distinta: MLP 6→32→24→9, con dos capas ocultas ReLU y salida Softmax. Sus seis entradas representan vector unitario hacia objetivo principal, vector secundario (amenaza para la presa o alimento para el depredador), energía y disponibilidad de objetivo. Las nueve salidas corresponden a ocho movimientos y quedarse quieto. El movimiento ejecutado proviene del argmax de la red neuronal para los agentes entrenados.

Se usa aprendizaje supervisado por imitación. Un experto vectorial genera etiquetas y la MLP aprende con entropía cruzada, mini lotes y retropropagación. Los pesos cambian durante el entrenamiento; `modelos/*.npz` conserva los pesos finales. No es aprendizaje por refuerzo: la regla experta proporciona los ejemplos. Se compara además una política aleatoria como referencia independiente.

## 3 Metodología y controles

Se generaron 12.000 estados sintéticos balanceados entre especies; cada especie tiene 4.800 muestras de entrenamiento y 1.200 de prueba (80/20), con semilla 42. Se entrenó durante 120 épocas, tasa 0,035 y arquitectura 6→32→24→9.

La evaluación del ecosistema usa 30 semillas (1000–1029) por cada combinación de escenario y política. Son 360 episodios en total: red entrenada, la misma red antes de entrenar, política experta de reglas y política aleatoria. Para cada semilla se compara la misma posición inicial entre políticas. Los episodios terminan cuando se extingue una especie o al llegar al máximo de 250 pasos. `evidencia/episodios.csv` conserva cada episodio; `evidencia/resumen.csv` incluye medias y desviaciones estándar muestrales de supervivencia, consumo, capturas, energías finales y duración. El tiempo hasta la primera captura se promedia solo entre episodios donde hubo capturas; cuando no las hay, el dato queda vacío.

**Hipótesis:** (H1) el entrenamiento reduce pérdida y aumenta la exactitud al imitar las etiquetas; (H2) una red más ancha aumenta la exactitud de prueba; (H3) las políticas neuronales aumentan supervivencia de presas frente a las referencias aleatorias y de reglas.

## 4 Resultados

### Comparación antes y después del entrenamiento

| Especie | Pérdida antes | Pérdida después | Exactitud antes | Exactitud después | Cambio L2 de pesos |
|---|---:|---:|---:|---:|
| Presa | 2,498 | 0,089 | 15,6 % | 97,7 % | 10,318 |
| Depredador | 2,484 | 0,059 | 14,7 % | 98,7 % | 8,582 |

**Variables controladas:** arquitectura, datos, partición, semilla y tasa; solo cambia el entrenamiento de 120 épocas. **Análisis:** la pérdida bajó y la exactitud subió marcadamente en ambos modelos. **Conclusión:** H1 se apoya para imitación de las etiquetas de prueba. El cambio L2 confirma que los parámetros sí se actualizaron. Esto prueba aprendizaje de la política de referencia, no que la política sea ecológicamente buena.

### Comparación de arquitecturas

Mismo conjunto de entrenamiento/prueba, semilla, tasa y épocas; solo cambia el ancho de las dos capas ocultas.

| Especie | Capas ocultas | Parámetros | Exactitud de prueba |
|---|---|---:|---:|
| Presa | 16–12 | 433 | 97,6 % |
| Presa | 32–24 | 1.241 | 97,7 % |
| Depredador | 16–12 | 433 | 99,1 % |
| Depredador | 32–24 | 1.241 | 98,7 % |

**Análisis:** la arquitectura ancha no mejoró de forma relevante la exactitud; en depredadores el modelo pequeño obtuvo mayor exactitud con cerca de un tercio de parámetros. **Conclusión:** H2 no se apoya. Para este conjunto, la arquitectura pequeña parece suficiente; se requiere medir también su desempeño ecológico antes de adoptarla como modelo final.

### Comparación de políticas por escenario

Media ± desviación estándar muestral, n=30. “Sobrevivientes” es la cantidad media de presas al terminar el episodio. Los finales pueden ocurrir antes de 250 pasos si una población se extingue.

| Escenario | Política | Presas supervivientes | Alimento consumido | Capturas |
|---|---|---:|---:|---:|
| Abundancia | Neuronal entrenada | 0,00 ± 0,00 | 6,23 ± 2,90 | 7,97 ± 1,50 |
| Abundancia | Neuronal sin entrenar | 5,03 ± 1,40 | 3,90 ± 1,84 | 0,60 ± 1,10 |
| Abundancia | Reglas expertas | 0,00 ± 0,00 | 6,37 ± 3,13 | 8,17 ± 1,18 |
| Abundancia | Aleatoria | 8,17 ± 1,72 | 26,60 ± 7,04 | 2,60 ± 1,69 |
| Escasez | Neuronal entrenada | 0,00 ± 0,00 | 2,60 ± 1,43 | 7,53 ± 1,52 |
| Escasez | Neuronal sin entrenar | 5,07 ± 1,39 | 1,83 ± 1,42 | 0,43 ± 0,86 |
| Escasez | Reglas expertas | 0,00 ± 0,00 | 2,43 ± 1,59 | 7,53 ± 1,31 |
| Escasez | Aleatoria | 8,20 ± 1,85 | 16,30 ± 4,96 | 2,40 ± 1,81 |
| Presión | Neuronal entrenada | 0,17 ± 0,65 | 4,17 ± 2,55 | 9,70 ± 1,44 |
| Presión | Neuronal sin entrenar | 6,57 ± 1,87 | 2,40 ± 1,48 | 1,33 ± 1,37 |
| Presión | Reglas expertas | 0,17 ± 0,91 | 3,50 ± 2,10 | 9,90 ± 1,65 |
| Presión | Aleatoria | 6,43 ± 1,68 | 19,80 ± 5,80 | 4,47 ± 1,63 |

**Métricas adicionales**

| Escenario | Política | Energía final presas | Energía final depredadores | Tiempo a primera captura |
|---|---|---:|---:|---:|
| Abundancia | Neuronal entrenada | 0,00 ± 0,00 | 0,85 ± 0,11 | 11,50 ± 5,03 pasos (n=30) |
| Abundancia | Neuronal sin entrenar | 0,49 ± 0,03 | 0,00 ± 0,00 | 6,40 ± 2,55 pasos (n=10) |
| Abundancia | Reglas expertas | 0,00 ± 0,00 | 0,84 ± 0,10 | 11,53 ± 4,86 pasos (n=30) |
| Abundancia | Aleatoria | 0,70 ± 0,08 | 0,00 ± 0,01 | 28,21 ± 23,96 pasos (n=28) |
| Escasez | Neuronal entrenada | 0,00 ± 0,00 | 0,85 ± 0,13 | 12,37 ± 5,38 pasos (n=30) |
| Escasez | Neuronal sin entrenar | 0,49 ± 0,03 | 0,00 ± 0,00 | 6,22 ± 2,73 pasos (n=9) |
| Escasez | Reglas expertas | 0,00 ± 0,00 | 0,86 ± 0,10 | 12,13 ± 5,04 pasos (n=30) |
| Escasez | Aleatoria | 0,65 ± 0,10 | 0,00 ± 0,00 | 22,15 ± 26,61 pasos (n=26) |
| Presión | Neuronal entrenada | 0,03 ± 0,10 | 0,66 ± 0,21 | 5,67 ± 4,49 pasos (n=30) |
| Presión | Neuronal sin entrenar | 0,46 ± 0,06 | 0,00 ± 0,00 | 8,47 ± 10,99 pasos (n=19) |
| Presión | Reglas expertas | 0,01 ± 0,06 | 0,68 ± 0,17 | 5,23 ± 3,31 pasos (n=30) |
| Presión | Aleatoria | 0,68 ± 0,08 | 0,00 ± 0,00 | 15,43 ± 14,81 pasos (n=30) |


**Contraste pareado de supervivencia**

Las políticas se compararon sobre las mismas 30 semillas. La diferencia se calcula como aleatoria menos neuronal entrenada; IC 95 % con t de Student (gl=29).

| Escenario | Diferencia media de supervivientes (aleatoria − neuronal entrenada) | IC 95 % pareado |
|---|---:|---:|
| Abundancia | 8,17 | 7,52 a 8,81 |
| Escasez | 8,20 | 7,51 a 8,89 |
| Presión | 6,27 | 5,70 a 6,84 |

**Análisis:** la red entrenada y el experto de reglas producen resultados cercanos, coherente con la alta exactitud de imitación. La aleatoria mantiene más presas en los tres escenarios: 8,17 frente a 0,00 en abundancia; 8,20 frente a 0,00 en escasez; y 6,43 frente a 0,17 en presión. En contraste, las políticas entrenadas acumulan más capturas. Las diferencias pareadas por semilla se muestran abajo con intervalos de confianza aproximados del 95 %. **Conclusión:** H3 se rechaza para supervivencia. La red sí modifica las decisiones y aprende la regla de referencia, pero esa imitación no da el mejor balance ecológico. Las energías, duración, causa de finalización y datos por semilla están en los CSV.

## 5 Discusión, limitaciones y mejoras

Los resultados muestran que imitar bien una regla no garantiza supervivencia. Las redes casi replican al experto; la aleatoria, al explorar más, mantiene más presas. Como solo reciben direcciones y energía, las redes ignoran distancias, congestión y obstáculos, posibles explicaciones del resultado.

El entrenamiento usa etiquetas sintéticas y no optimiza directamente la supervivencia; la evaluación tampoco demuestra generalización a otros mapas. El siguiente paso es añadir percepción del entorno y ejemplos con penalización de colisiones, y repetir las mismas semillas para comprobar el efecto.
## 6 Reproducibilidad y uso de IA

Instalación y ejecución: instrucciones en `README.md`. Las semillas, parámetros, datos episodio a episodio y pesos están incluidos. Para recrear modelos y evidencia, ejecutar `python -m neurito_ecosistema.experimentos` desde esta carpeta. La evidencia fue generada con Python 3.12 y NumPy del entorno del proyecto de clase.

Se utilizó un asistente de programación para organizar código, documentación y análisis inicial. El equipo debe revisar y explicar el MLP, la retropropagación, las reglas que generan etiquetas y los resultados antes de la sustentación; debe declarar cambios que acepte o rechace y repetir las ejecuciones en su propio entorno.



