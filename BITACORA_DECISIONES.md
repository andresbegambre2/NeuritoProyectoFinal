# Bitácora de decisiones técnicas

| # | Decisión | Alternativas consideradas | Criterio y evidencia prevista |
|---|---|---|---|
| 1 | Representar el ecosistema en una cuadrícula 24×24 | Coordenadas continuas; cuadrícula | Facilita reproducir posiciones, obstáculos y movimientos en cada semilla. |
| 2 | Usar dos modelos separados por especie | Una red compartida con indicador de especie | Presas y depredadores optimizan objetivos distintos; modelos separados permiten comparar comportamiento y parámetros. |
| 3 | Usar seis entradas geométricas y de estado | Codificar el tablero completo | Vectores unitarios al objetivo/amenaza y energía son interpretables y mantienen una entrada pequeña. Se reconoce que omiten rutas y distribución global. |
| 4 | Usar MLP 6→32→24→9 con ReLU y Softmax | Una sola capa; más capas; Q-learning | Conserva la implementación NumPy vista en clase y cumple dos capas ocultas. Softmax con entropía cruzada permite imitación supervisada verificable. |
| 5 | Entrenar con etiquetas de experto vectorial | Aprendizaje por refuerzo o neuroevolución | Es entrenable con recursos limitados y permite comparación explícita contra el experto. La red imita heurísticas, no descubre autonomía general. |
| 6 | Mantener política aleatoria y experto como líneas base | Comparar solo redes | Distingue aprendizaje de movimiento al azar y de comportamiento de regla. Las mismas semillas y escenarios controlan la comparación. |
| 7 | Evaluar tres escenarios, diez semillas y 250 pasos | Una partida demostrativa | Reduce dependencia de una sola corrida y hace visibles abundancia, escasez y presión de depredación. |
| 8 | Ajustar desgaste energético y regeneración | Mantener desgaste inicial alto | La primera corrida causó extinción casi total; se redujo el desgaste y se aumentó regeneración para medir diferencias sin ocultar la sensibilidad del sistema. La primera corrida se conserva como antecedente en el historial conversacional, no como resultado final. |
| 9 | Registrar semillas, configuración y datos por episodio | Reportar promedios solamente | `episodios.csv` conserva el detalle para recalcular tablas y analizar variabilidad. |

## Controles experimentales

Cada grupo de comparación reutiliza escenario, horizonte, tamaño de población y diez semillas predefinidas. La fuente de datos supervisados usa semilla 42 y una partición 80/20. Para arquitectura, se conserva el conjunto y se cambia únicamente el ancho de las dos capas ocultas. Las ejecuciones son deterministas con la versión de NumPy usada al generarlas.
