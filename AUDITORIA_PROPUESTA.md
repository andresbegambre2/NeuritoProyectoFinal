# Auditoría de cumplimiento de la propuesta

**Documento revisado:** Proyecto Final Integrador NeuroEcosistema – Depredadores y Presas.  
**Resultado:** la carpeta contiene los productos técnicos y experimentales solicitados. El resultado conductual es negativo para la hipótesis de superioridad neuronal en supervivencia, pero la propuesta permite resultados negativos cuando están reproducidos, medidos e interpretados. La sustentación individual sigue siendo responsabilidad del equipo.

| Requisito del profesor | Evidencia de la entrega | Estado y observación |
|---|---|---|
| Simulación 2D con alimento, energía, movimiento, capturas y fin de episodio | `neurito_ecosistema/ecosistema.py`; final por extinción de una especie o límite de 250 pasos | Cumple |
| Dos especies con objetivos y decisiones diferenciados | Modelos separados; la salida de cada MLP selecciona el movimiento durante la política neuronal | Cumple |
| MLP por especie con al menos dos capas ocultas | 6→32→24→9, dos capas ocultas ReLU y salida Softmax | Cumple |
| Entrenamiento real y evidencia de parámetros modificados | Aprendizaje supervisado por imitación; pérdida, exactitud y cambio L2 registrados en `modelos/training_summary.json` | Cumple; las etiquetas son de un experto vectorial y los estados son sintéticos, no aprendizaje por refuerzo |
| Comparar antes/después del entrenamiento, configuraciones y referencia no neuronal | Informe técnico; red entrenada/sin entrenar, reglas y política aleatoria | Cumple; la comparación de arquitectura se hace sobre exactitud de imitación. El desempeño ecológico de la arquitectura pequeña queda como trabajo futuro |
| Tres escenarios ambientales requeridos | Abundancia, escasez y presión con más depredadores/obstáculos | Cumple |
| Repeticiones, semillas y métricas | 30 semillas emparejadas por escenario y política; 360 episodios; CSV por episodio y resumen con desviaciones estándar e IC pareado | Cumple y supera el mínimo de varias ejecuciones |
| Visualización, estadísticas y consulta de decisiones | Aplicación Pygame con controles, poblaciones, consumo, capturas, energía y decisión neuronal de muestra | Cumple |
| Reproducibilidad | README, requisitos, semillas, pesos entrenados y scripts de ejecución | Cumple |
| Justificación de al menos seis decisiones | `BITACORA_DECISIONES.md`, nueve decisiones con alternativas y criterio | Cumple |
| Informe de máximo diez páginas con análisis experimental | `INFORME_TECNICO.docx` y PDF; preguntas, hipótesis, controles, tablas, interpretaciones y limitaciones | Cumple; 3 páginas, dentro del máximo de 10 |
| Declaración de uso de IA | Sección en el informe y README | Cumple; el equipo debe explicar qué revisó y validó |
| Repositorio con código y productos | Repositorio GitHub privado NeuritoProyectoFinal | Cumple; contiene solo la carpeta de entrega del proyecto final |
| Demostración en vivo y preguntas individuales | Controles de la aplicación y guía del informe | Pendiente de realizar; cada integrante debe poder explicar la red, entrenamiento, métricas y decisiones |

## Conclusión experimental que se debe presentar

La red entrenada imita con alta exactitud al experto y produce más capturas, pero en las 30 semillas la política aleatoria deja más presas al final en los tres escenarios. Por tanto, no se debe afirmar que la red mejora la supervivencia. El hallazgo muestra que exactitud de imitación y desempeño ecológico son objetivos distintos. La percepción local omite distancias, densidad y planificación frente a obstáculos; estas son mejoras justificadas por los resultados.

## Preparación pendiente del equipo

1. Ejecutar la demostración y explicar los controles.
2. Cada integrante debe explicar qué son las entradas, salidas, dos capas ocultas, ReLU, Softmax y retropropagación.
3. Defender por qué se usó imitación supervisada y reconocer lo que los datos sintéticos no demuestran.
4. Leer el CSV y explicar una diferencia media y su desviación/intervalo.
5. Declarar con honestidad el apoyo de IA y qué componentes revisó y verificó el equipo.

