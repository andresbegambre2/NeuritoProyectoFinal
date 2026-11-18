# Informe técnico: NeuroEcosistema Neurito

**Universidad Santo Tomás, seccional Tunja · Electiva de Inteligencia Artificial**  
**Proyecto:** simulación de depredadores y presas  
**Fecha de generación de evidencia:** 18 de noviembre de 2026

## 1. Problema y objetivo

Se implementó una simulación 2D donde presas buscan alimento y evitan depredadores, mientras los depredadores persiguen presas y recuperan energía al capturarlas. La pregunta experimental es si agentes con redes neuronales obtienen mejor desempeño que políticas sin aprendizaje en escenarios con recursos suficientes, escasez y presión de depredación/obstáculos.

## 2. Diseño e implementación

El mundo es una cuadrícula de 24×24 con 12 presas iniciales. Los escenarios son: abundancia (22 alimentos, 2 depredadores, sin obstáculos), escasez (7 alimentos, 2 depredadores), y presión (16 alimentos, 5 depredadores y 18 obstáculos). El alimento puede regenerarse. La energía se consume por paso y se recupera al comer o capturar.

Cada especie tiene una red neuronal distinta: MLP 6→32→24→9, con dos capas ocultas ReLU y salida Softmax. Sus seis entradas representan vector unitario hacia objetivo principal, vector secundario (amenaza para la presa o alimento para el depredador), energía y disponibilidad de objetivo. Las nueve salidas corresponden a ocho movimientos y quedarse quieto. El movimiento ejecutado proviene del argmax de la red neuronal para los agentes entrenados.

Se usa aprendizaje supervisado por imitación. Un experto vectorial genera etiquetas y la MLP aprende con entropía cruzada, mini lotes y retropropagación. Los pesos cambian durante el entrenamiento; `modelos/*.npz` conserva los pesos finales. No es aprendizaje por refuerzo: la regla experta proporciona los ejemplos. Se compara además una política aleatoria como referencia independiente.

## 3. Metodología y controles

Se generaron 12.000 estados sintéticos balanceados entre especies; cada especie tiene 4.800 muestras de entrenamiento y 1.200 de prueba (80/20), con semilla 42. Se entrenó durante 120 épocas, tasa 0,035 y arquitectura 6→32→24→9.

La evaluación de ecosistema usa 10 semillas (1000–1009) por cada combinación de escenario y política, durante 250 pasos. Son 120 episodios en total: red entrenada, la misma red antes de entrenar, política experta de reglas y política aleatoria. Se mantienen iguales escenario, población inicial, horizonte y semillas. El archivo `evidencia/episodios.csv` registra cada episodio, incluidas capturas, consumo y tiempo hasta la primera captura; `evidencia/resumen.csv` incluye promedios y desviaciones estándar muestrales.

**Hipótesis:** (H1) el entrenamiento reduce pérdida y aumenta la exactitud al imitar las etiquetas; (H2) una red más ancha aumenta la exactitud de prueba; (H3) las políticas neuronales aumentan supervivencia de presas frente a las referencias aleatorias y de reglas.

## 4. Resultados

### Comparación antes y después del entrenamiento (H1)

| Especie | Pérdida antes | Pérdida después | Exactitud antes | Exactitud después | Cambio L2 de pesos |
|---|---:|---:|---:|---:|
| Presa | 2,498 | 0,089 | 15,6 % | 97,7 % | 10,318 |
| Depredador | 2,484 | 0,059 | 14,7 % | 98,7 % | 8,582 |

**Variables controladas:** arquitectura, datos, partición, semilla y tasa; solo cambia el entrenamiento de 120 épocas. **Análisis:** la pérdida bajó y la exactitud subió marcadamente en ambos modelos. **Conclusión:** H1 se apoya para imitación de las etiquetas de prueba. El cambio L2 confirma que los parámetros sí se actualizaron. Esto prueba aprendizaje de la política de referencia, no que la política sea ecológicamente buena.

### Comparación de arquitecturas (H2)

Mismo conjunto de entrenamiento/prueba, semilla, tasa y épocas; solo cambia el ancho de las dos capas ocultas.

| Especie | Capas ocultas | Parámetros | Exactitud de prueba |
|---|---|---:|---:|
| Presa | 16–12 | 433 | 97,6 % |
| Presa | 32–24 | 1.241 | 97,7 % |
| Depredador | 16–12 | 433 | 99,1 % |
| Depredador | 32–24 | 1.241 | 98,7 % |

**Análisis:** la arquitectura ancha no mejoró de forma relevante la exactitud; en depredadores el modelo pequeño obtuvo mayor exactitud con cerca de un tercio de parámetros. **Conclusión:** H2 no se apoya. Para este conjunto, la arquitectura pequeña parece suficiente; se requiere medir también su desempeño ecológico antes de adoptarla como modelo final.

### Comparación de políticas por escenario (H3)

Promedios por episodio, n=10. “Sobrevivientes” es la cantidad media de presas vivas al paso 250; capturas y alimento son totales por episodio.

| Escenario | Política | Presas sobrevivientes | Alimento consumido | Capturas |
|---|---|---:|---:|---:|
| Abundancia | Neuronal entrenada | 0,0 | 5,2 | 8,1 |
| Abundancia | Neuronal sin entrenar | 0,0 | 3,5 | 0,7 |
| Abundancia | Reglas expertas | 0,0 | 5,2 | 8,1 |
| Abundancia | Aleatoria | 7,8 | 53,9 | 1,8 |
| Escasez | Neuronal entrenada | 0,0 | 2,9 | 6,9 |
| Escasez | Neuronal sin entrenar | 0,0 | 2,0 | 0,2 |
| Escasez | Reglas expertas | 0,0 | 2,4 | 7,3 |
| Escasez | Aleatoria | 5,4 | 37,1 | 2,9 |
| Presión | Neuronal entrenada | 0,2 | 9,7 | 9,4 |
| Presión | Neuronal sin entrenar | 0,1 | 2,5 | 0,7 |
| Presión | Reglas expertas | 0,4 | 9,5 | 9,7 |
| Presión | Aleatoria | 5,0 | 37,3 | 4,5 |

**Análisis:** la red entrenada supera claramente a su versión no entrenada en capturas y alimento, pero la aleatoria mantiene más presas y consume más alimento en los tres escenarios. La red entrenada y el experto de reglas son casi equivalentes, coherente con su alta exactitud de imitación. En abundancia y escasez, la extinción de presas neuronales fue consistente en las diez semillas; en presión hubo supervivencia media de 0,2. **Conclusión:** H3 se rechaza. La red sí modifica decisiones de forma verificable, pero el objetivo de imitación vectorial conduce a un desempeño ecológico débil. Las tablas de desviación estándar y el tiempo a primera captura están en `evidencia/resumen.csv`.

## 5. Discusión, limitaciones y mejoras

El contraste más importante es que alta exactitud de clasificación no garantiza supervivencia. Las entradas solo incluyen direcciones locales y energía: no codifican caminos, congestión, memoria ni distancia a obstáculos. Cuando múltiples agentes siguen un vector parecido, pueden competir por casillas o quedar atrapados. La política aleatoria explora el tablero y encuentra alimento con más frecuencia, aunque captura menos presas. Los depredadores neuronales capturan más que los aleatorios, lo que sugiere persecución efectiva con el coste de extinguir a las presas.

El modelo de reglas actúa como etiqueta de entrenamiento y referencia; por ello, que la red la iguale no constituye validación independiente. El entorno no incorpora reproducción, edad ni adaptación durante los episodios. Los resultados dependen de la discretización y de diez semillas; no deben generalizarse a ecosistemas reales. Las conclusiones describen los datos observados y no reclaman superioridad neuronal.

La primera mejora recomendada es añadir percepción de obstáculos y densidad local, y penalizar colisiones; después entrenar con ejemplos de trayectorias exitosas o una recompensa explícita de supervivencia y alimento. Se deben volver a ejecutar las mismas semillas y reportar intervalos/variabilidad para comprobar si mejora la supervivencia sin eliminar capturas.

## 6. Reproducibilidad y uso de IA

Instalación y ejecución: instrucciones en `README.md`. Las semillas, parámetros, datos episodio a episodio y pesos están incluidos. Para recrear modelos y evidencia, ejecutar `python -m neurito_ecosistema.experimentos` desde esta carpeta. La evidencia fue generada con Python 3.12 y NumPy del entorno del proyecto de clase.

Se utilizó un asistente de programación para organizar código, documentación y análisis inicial. El equipo debe revisar y explicar el MLP, la retropropagación, las reglas que generan etiquetas y los resultados antes de la sustentación; debe declarar cambios que acepte o rechace y repetir las ejecuciones en su propio entorno.

