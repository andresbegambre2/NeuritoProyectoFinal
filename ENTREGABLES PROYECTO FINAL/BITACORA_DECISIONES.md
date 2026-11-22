# Bitácora de decisiones técnicas

Esta bitácora registra por qué elegí los componentes principales y qué evidencia usé para revisarlos. Las decisiones se pueden contrastar con el código y con los resultados guardados en `evidencia/`.

| # | Decisión | Alternativas consideradas | Por qué la elegí y qué evidencia tengo |
|---|---|---|---|
| 1 | Usar una cuadrícula de 24×24 | Coordenadas continuas o un tablero discreto | La cuadrícula hace sencillo registrar posiciones, obstáculos y alimento con la misma semilla. Los escenarios y episodios guardados usan este tamaño. La desventaja es que los agentes solo se mueven por casillas. |
| 2 | Entrenar una red distinta para cada especie | Compartir una red e indicar el tipo de agente como entrada | Las presas y los depredadores tienen objetivos diferentes. Los archivos `prey_model.npz` y `predator_model.npz` conservan sus parámetros por separado, y el resumen de entrenamiento registra sus resultados individualmente. |
| 3 | Dar a cada red seis entradas locales | Codificar todas las casillas del tablero | Las entradas describen direcciones hacia objetivos cercanos, energía y disponibilidad de objetivo. Elegí esta representación porque mantiene pequeña la red y es fácil de explicar. Su límite es que no incluye distancias exactas, congestión ni rutas para rodear obstáculos. |
| 4 | Usar una MLP 6→32→24→9, con ReLU y Softmax | Una capa oculta, otros tamaños o aprendizaje por refuerzo | Esta arquitectura tiene las dos capas ocultas pedidas y se puede entrenar con el MLP de NumPy. La comparación guardada muestra que aumentar el tamaño casi no mejora la imitación: la red pequeña obtuvo 97,6 % y 99,1 % de exactitud; la grande, 97,7 % y 98,7 %. |
| 5 | Entrenar por imitación supervisada de una regla vectorial | Neuroevolución o aprendizaje por refuerzo | La regla produce ejemplos reproducibles y permite comprobar si los pesos cambian. La pérdida y la exactitud mejoraron después del entrenamiento. Este resultado mide qué tan bien se imita la regla; no significa que la red haya aprendido por recompensas ni que encuentre la mejor estrategia ecológica. |
| 6 | Comparar red entrenada, red sin entrenar, reglas y política aleatoria | Comparar únicamente la red con la regla | La red sin entrenar ayuda a ver el efecto del ajuste; las reglas muestran la política que genera las etiquetas; la aleatoria sirve como referencia sin aprendizaje. En cada condición se asigna la política a ambas especies, así que la comparación se refiere al ecosistema completo. |
| 7 | Evaluar tres escenarios con 30 semillas y tope de 250 pasos | Analizar una sola partida o usar pocas repeticiones | Los escenarios cubren abundancia, escasez y presión de depredación. Las mismas semillas iniciales (1000–1029) permiten comparar políticas desde estados equivalentes y observar variación entre corridas. Los CSV conservan los 360 episodios. |
| 8 | Ajustar el gasto de energía y la regeneración de alimento | Mantener el desgaste inicial más alto | En las corridas finales fijé un gasto de 0,006 por paso para las presas, 0,012 para los depredadores y regeneración de alimento de 0,25 por paso. En el repositorio no hay una comparación entre valores alternativos de energía; por eso registro los parámetros usados, pero no afirmo que sean óptimos. |
| 9 | Guardar semillas, configuración y datos por episodio | Publicar solo promedios | `episodios.csv` permite revisar cada corrida y `resumen.csv` facilita comparar medias y desviaciones. También se guardan los pesos y el historial de entrenamiento para que los resultados se puedan revisar. |

## Cómo controlé las comparaciones

En cada grupo mantuve el escenario, las posiciones iniciales, el número de agentes y el límite de 250 pasos. Cambié la política entre condiciones y repetí la comparación con 30 semillas. Para medir la arquitectura mantuve los datos, la partición, la semilla, la tasa de aprendizaje y las épocas; cambié el número de neuronas ocultas. El conjunto supervisado se generó con la semilla 42 y se dividió en 80 % para entrenamiento y 20 % para prueba.

## Qué aprendí de estas decisiones

La red entrenada aprendió a imitar la regla, pero la política aleatoria dejó más presas vivas en los tres escenarios. Este resultado me hizo separar dos preguntas que al principio podían parecer iguales: qué tan bien imita una red y qué tan conveniente es su comportamiento para el ecosistema. Para la siguiente versión probaría cada especie por separado y añadiría información sobre distancias y obstáculos.
