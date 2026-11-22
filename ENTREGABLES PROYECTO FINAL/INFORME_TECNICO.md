# Informe técnico del NeuroEcosistema de presas y depredadores

**Universidad Santo Tomás, seccional Tunja · Electiva I de Profundización – Inteligencia Artificial**

**Docente:** Diego Alejandro Vela Beltrán

**Autor:** Andrés Leonardo Begambre Vargas

**Proyecto:** simulación de depredadores y presas

**Fecha de generación de evidencia:** 20 de noviembre de 2026

En este trabajo construí una simulación de presas y depredadores y la comparé en 360 episodios. La red aprendió a imitar la regla experta. En mis pruebas la política aleatoria dejó más presas vivas. Por eso no concluyo que la red haya mejorado la supervivencia. En este informe explico qué medí, qué encontré y qué aspectos todavía limitan el modelo.

## 1 Problema y objetivo

Partí de una pregunta concreta: ¿una red neuronal ayuda a que los agentes se comporten mejor que una política aleatoria o una regla fija? Para explorarla, configuré las presas para buscar alimento y evitar amenazas, y los depredadores para perseguir presas y recuperar energía al capturarlas. Medí el comportamiento en condiciones de abundancia, escasez y mayor presión de depredación.

## 2 Diseño e implementación

Usé un tablero de 24×24 y cada episodio comienza con 12 presas. Preparé tres condiciones: abundancia, con 22 alimentos y 2 depredadores; escasez, con 7 alimentos y 2 depredadores; y presión, con 16 alimentos, 5 depredadores y 18 obstáculos. El alimento puede reaparecer durante la partida. Las dos poblaciones gastan energía al moverse y la recuperan al comer o capturar.

Implementé una red MLP para cada especie, con arquitectura 6→32→24→9. Tiene dos capas ocultas con activación ReLU y una salida Softmax. Las entradas representan la dirección al objetivo más cercano, una segunda dirección, la energía disponible y si hay objetivo. En las presas, la segunda dirección apunta en sentido contrario al depredador más cercano; en los depredadores, apunta al alimento. La regla de entrenamiento del depredador no usa esa dirección al alimento para crear sus etiquetas, así que esa entrada todavía no guía su aprendizaje. La red elige entre ocho movimientos y quedarse quieta. En la política neuronal, esa salida determina la acción que se ejecuta.

Entrené las redes por aprendizaje supervisado: una regla vectorial genera ejemplos y la MLP aprende a imitar sus decisiones mediante entropía cruzada y retropropagación por mini lotes. Guardé los pesos finales en `modelos/*.npz`. Este método sí modifica los parámetros, pero no es aprendizaje por refuerzo: la red aprende de la regla experta y no de recompensas obtenidas en el ecosistema.

## 3 Metodología y controles

Para entrenar utilicé 12.000 estados sintéticos, repartidos por igual entre las dos especies. En cada una reservé 4.800 ejemplos para entrenamiento y 1.200 para prueba. Fijé la semilla 42, 120 épocas y una tasa de aprendizaje de 0,035. La partición de prueba permite medir qué tan bien la red imita ejemplos que no vio durante el ajuste.

Probé cuatro políticas en cada escenario: red entrenada, la misma inicialización antes de entrenar, regla experta y movimiento aleatorio. Repetí cada combinación con 30 semillas, de la 1000 a la 1029; así comparé las políticas desde las mismas posiciones iniciales. En total son 360 episodios. Cada uno termina si se extingue una población o al llegar a 250 pasos. En cada condición apliqué la política elegida tanto a presas como a depredadores; por eso esta comparación mide el efecto de cambiar el control del ecosistema completo, no el efecto aislado de la red de una sola especie. `evidencia/episodios.csv` guarda cada corrida y `evidencia/resumen.csv` presenta los promedios y la variación. El tiempo hasta la primera captura solo se calcula cuando hubo captura.

Antes de revisar los resultados planteé tres expectativas: (H1) entrenar reduciría la pérdida y mejoraría la imitación de las etiquetas; (H2) la red más ancha tendría mayor exactitud de prueba; y (H3) las políticas neuronales dejarían más presas vivas que las reglas y el movimiento aleatorio.

## 4 Resultados

### Comparación antes y después del entrenamiento

| Especie | Pérdida antes | Pérdida después | Exactitud antes | Exactitud después | Cambio L2 de pesos |
|---|---:|---:|---:|---:|
| Presa | 2,498 | 0,089 | 15,6 % | 97,7 % | 10,318 |
| Depredador | 2,484 | 0,059 | 14,7 % | 98,7 % | 8,582 |

En esta comparación mantuve la arquitectura, los datos, la partición, la semilla y la tasa de aprendizaje; la diferencia fue entrenar durante 120 épocas. La pérdida disminuyó y la exactitud de prueba llegó a 97,7 % en presas y 98,7 % en depredadores. También cambió el conjunto de pesos. Estos resultados respaldan H1: las redes aprendieron a imitar las etiquetas. No muestran, por sí solos, que esa conducta sea mejor para el ecosistema.

### Comparación de arquitecturas

Mismo conjunto de entrenamiento/prueba, semilla, tasa y épocas; solo cambia el ancho de las dos capas ocultas.

| Especie | Capas ocultas | Parámetros | Exactitud de prueba |
|---|---|---:|---:|
| Presa | 16–12 | 433 | 97,6 % |
| Presa | 32–24 | 1.241 | 97,7 % |
| Depredador | 16–12 | 433 | 99,1 % |
| Depredador | 32–24 | 1.241 | 98,7 % |

La red más grande casi no cambió la exactitud de las presas y obtuvo una exactitud algo menor en depredadores. La versión pequeña usa 433 parámetros, frente a 1.241 en la grande. Con estos datos no se cumple H2. La red pequeña parece suficiente para imitar al experto, aunque todavía faltaría comparar su comportamiento dentro del ecosistema antes de elegirla como modelo final.

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

La red entrenada y la regla experta se comportaron de forma parecida, como era esperable por la alta exactitud de imitación. La política aleatoria dejó más presas vivas en los tres escenarios: 8,17 frente a 0,00 en abundancia; 8,20 frente a 0,00 en escasez; y 6,43 frente a 0,17 en presión. La red y las reglas, en cambio, lograron más capturas. Las diferencias entre corridas emparejadas aparecen con intervalos de confianza del 95 %. En `evidencia/graficas/` dejé una gráfica de supervivencia y otra con la pérdida de entrenamiento para ver estos patrones de un vistazo. Con estos resultados rechazo H3 para supervivencia: imitar bien una regla no bastó para lograr un mejor equilibrio. Los archivos CSV permiten consultar las demás métricas y cada episodio.

## 5 Discusión, fallos y mejoras

El principal problema que mostraron las pruebas no fue que la red dejara de aprender; fue que el entrenamiento solo le pedía imitar las etiquetas del experto. Por eso, obtener 97–99 % de exactitud no se tradujo en más presas vivas: la política aleatoria dejó más presas en los tres escenarios. Las entradas describen direcciones locales y energía, pero no la distancia exacta, la congestión ni las rutas alrededor de obstáculos. Además, cambié a la vez el control de presas y depredadores, así que no puedo atribuir la diferencia a una sola especie.

El entrenamiento usa ejemplos sintéticos y busca acertar la etiqueta del experto; no optimiza directamente la supervivencia ni demuestra que la red funcione igual en mapas distintos. Como siguiente paso propongo probar cada especie por separado, añadir información sobre obstáculos y distancia, y comparar de nuevo con las mismas semillas. Los archivos finales no incluyen una comparación entre distintos valores de energía; por eso no puedo afirmar que los parámetros elegidos sean óptimos.
## 6 Reproducibilidad y uso de IA

El proyecto se puede ejecutar con las instrucciones del `README.md`. Incluí las semillas, los parámetros, los resultados por episodio y los pesos finales. Para volver a entrenar las redes y generar la evidencia, se ejecuta `python -m neurito_ecosistema.experimentos` desde la carpeta del proyecto. Las corridas que acompañan este informe se hicieron con Python 3.12 y NumPy.

Desarrollé el proyecto con apoyo de Codex, un asistente de programación. Lo usé para revisar y completar parte del código, organizar las pruebas y preparar la documentación. Yo revisé la propuesta y ejecuté la aplicación en mi computador. Acepté ayuda para organizar la comparación de políticas; no tomé la exactitud de imitación como prueba de que la red mejorara la supervivencia, porque los resultados muestran lo contrario. Las cifras del informe se contrastaron con `evidencia/episodios.csv`, `evidencia/resumen.csv` y `modelos/training_summary.json`. Yo presento y respondo por las decisiones del proyecto; por eso debo poder explicar cómo funciona el entrenamiento y qué muestran sus resultados.
