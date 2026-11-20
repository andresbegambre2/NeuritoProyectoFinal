# NeuroEcosistema Neurito

Simulador 2D de presas y depredadores con dos redes neuronales multicapa entrenadas por aprendizaje supervisado. Reutiliza conceptos trabajados en clase: MLP en NumPy, ReLU, Softmax, retropropagación, Pygame y experimentación reproducible.

## Requisitos y ejecución

- Python 3.12 o superior
- NumPy 2.x
- Pygame CE 2.x (para la vista)

Desde esta carpeta en Windows:

```powershell
python -m pip install -r requirements.txt
python -m neurito_ecosistema.visualizar
```

La vista carga los modelos ya incluidos. Para volver a entrenar los modelos y regenerar los experimentos:

```powershell
python -m neurito_ecosistema.experimentos
```

## Diseño del ecosistema

El tablero es una cuadrícula de 24×24 con 12 presas iniciales. Hay tres escenarios: abundancia (22 alimentos, 2 depredadores, sin obstáculos), escasez (7 alimentos, 2 depredadores) y presión (16 alimentos, 5 depredadores y 18 obstáculos). El alimento se regenera; los agentes consumen energía y la recuperan al comer o capturar. Los episodios terminan si se extingue una especie o al alcanzar el límite de 250 pasos.

Cada especie usa una MLP 6→32→24→9, con dos capas ocultas ReLU y salida Softmax. Las entradas codifican direcciones al objetivo principal y secundario, energía y disponibilidad del objetivo. Las salidas representan ocho movimientos posibles y quedarse quieto. En la política neuronal, la acción se escoge con el valor más alto de salida de la red.

El entrenamiento es supervisado por imitación: una regla vectorial genera etiquetas y la red aprende con entropía cruzada y retropropagación por mini lotes. No es aprendizaje por refuerzo. La política de reglas es tanto referencia como fuente de las etiquetas; la aleatoria es una referencia independiente.

## Experimentos reproducibles

Se comparan cuatro políticas: red entrenada, la misma red antes del entrenamiento, reglas y movimiento aleatorio. Hay 3 escenarios × 4 políticas × 30 semillas = **360 episodios**. Las semillas 1000–1029 emparejan las posiciones iniciales entre políticas. Cada episodio dura hasta 250 pasos o termina por extinción de una especie.

Se registran supervivientes, alimento consumido, capturas, energía final de presas y depredadores, duración, motivo de terminación y tiempo hasta la primera captura. Para el tiempo a la primera captura, los promedios consideran solo episodios donde ocurrió al menos una captura; en los demás queda vacío, no cero. Los CSV contienen resultados por episodio, promedios y desviaciones estándar.

La comparación de arquitecturas (16–12 y 32–24 neuronas ocultas) usa los mismos datos, semillas, tasa y épocas. Los resultados son descriptivos de este modelo y estas semillas. Alta exactitud al imitar reglas no demuestra por sí sola un mejor desempeño ecológico.

## Vista interactiva

`visualizar.py` abre Pygame. ESPACIO inicia o pausa; flecha derecha avanza un paso pausado; N cambia escenario; P alterna entre política neuronal, aleatoria y reglas; R reinicia la misma semilla; ESC sale. El panel muestra las poblaciones, alimento consumido, capturas, energía de presas y estado de episodio.

## Archivos de entrega

- `neurito_ecosistema/`: entorno, MLP, entrenamiento, experimentos y vista.
- `modelos/`: pesos entrenados y resumen del entrenamiento.
- `evidencia/`: episodios individuales y resúmenes experimentales.
- `INFORME_TECNICO.docx` y `INFORME_TECNICO.pdf`: informe.
- `INFORME_TECNICO.md`: fuente editable del informe.
- `BITACORA_DECISIONES.md`: decisiones justificadas.
- `AUDITORIA_PROPUESTA.md`: revisión requisito por requisito y puntos pendientes para la sustentación.
- `INICIAR_SIMULACION.bat` y `GENERAR_EVIDENCIA.bat`: accesos rápidos para Windows.

## Uso de IA

Se utilizó un asistente de programación para apoyar la implementación y la documentación. El equipo debe comprender, verificar y declarar qué herramientas empleó, qué recomendaciones aceptó y qué validaciones realizó.



