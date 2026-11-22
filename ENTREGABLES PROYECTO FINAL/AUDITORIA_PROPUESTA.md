# Revisión de requisitos del proyecto

Revisé los requisitos de la propuesta frente al código, los modelos y la evidencia guardada en este repositorio. El trabajo incluye la simulación, las comparaciones experimentales y un informe con resultados y límites. El resultado que no favorece a la red neuronal también se presenta: la propuesta permite resultados negativos si se explican con datos.

| Lo que pide la propuesta | Dónde se puede revisar | Estado |
|---|---|---|
| Simulación 2D con alimento, energía, movimiento, capturas y fin de episodio | `../neurito_ecosistema/ecosistema.py` | Implementado |
| Dos especies con objetivos y redes diferenciadas | `../neurito_ecosistema/entrenar.py`; pesos en `../modelos/` | Implementado; cada MLP selecciona acciones durante la política neuronal |
| Dos capas ocultas como mínimo y entradas/salidas documentadas | Informe técnico y `../neurito_ecosistema/red.py` | Documentado: 6→32→24→9, ReLU y Softmax |
| Entrenamiento real y cambio de parámetros | `../modelos/training_summary.json` y `.npz` | Registrado con aprendizaje supervisado por imitación |
| Comparación antes/después, entre configuraciones y frente a una referencia | Informe, `evidencia/resumen.csv`, `evidencia/resumen.json` | Incluida; la comparación de arquitectura mide exactitud de imitación, no rendimiento ecológico |
| Tres escenarios y varias ejecuciones con semillas | `evidencia/episodios.csv` | 30 semillas por política y escenario, 360 episodios |
| Métricas y datos que permitan revisar las conclusiones | CSV, JSON y gráficas en `evidencia/` | Incluidos; supervivencia, alimento, capturas, energía, duración y variación |
| Aplicación visible con controles y variables | `../neurito_ecosistema/visualizar.py` | El autor confirmó que ya la ejecutó en su computador; debe volver a abrirla para la sustentación |
| Instrucciones y dependencias | `../README.md` y `../requirements.txt` | Incluidas |
| Bitácora con seis o más decisiones | `BITACORA_DECISIONES.md` | Incluye nueve decisiones y sus alternativas |
| Informe de hasta diez páginas con análisis, límites y recomendaciones | `INFORME_TECNICO.docx` y PDF | Incluido; cuatro páginas, dentro del máximo de diez. Se revisó el PDF después de actualizarlo |
| Declaración de uso de IA, finalidad, decisiones y verificación | Sección 6 del informe | Incluida; leerla antes de entregar y estar preparado para explicar el apoyo recibido |
| Repositorio con código y productos | Repositorio NeuritoProyectoFinal | Incluido en la carpeta del repositorio |
| Demostración en vivo y preguntas individuales | Aplicación y sustentación | Pendiente de realizar en clase |

## Resultado que conviene explicar

La red entrenada imita bien la regla experta y produce muchas capturas. Aun así, la política aleatoria terminó con más presas vivas en las tres condiciones. No presento este resultado como una mejora de la red. En cada condición experimental cambié la política de las dos especies a la vez, así que los datos comparan ecosistemas completos y no separan el efecto de la política de presas del efecto de la política de depredadores.

## Aspectos que todavía requieren atención

- La red se entrenó con estados sintéticos y etiquetas creadas por una regla; no aprendió directamente de recompensas del ecosistema.
- La comparación de las dos arquitecturas mide exactitud de imitación. Su rendimiento ecológico aún no se comparó.
- No hay en el repositorio una comparación de sensibilidad para justificar los valores de gasto de energía y regeneración frente a otras opciones. Se describen como parámetros usados, no como valores óptimos.
- La sustentación y las preguntas individuales no se pueden marcar como realizadas hasta que ocurran.
- El Word y el PDF finales se revisaron visualmente; el informe tiene cuatro páginas y está dentro del límite de diez.
