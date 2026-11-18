# NeuroEcosistema Neurito

Simulador 2D de presas y depredadores con dos redes neuronales multicapa entrenadas por aprendizaje supervisado. Reutiliza conceptos y código de clase: perceptrones multicapa implementados con NumPy, activaciones ReLU/Softmax, retropropagación, Pygame y experimentos reproducibles.

## Requisitos y ejecución

- Python 3.12 o superior
- NumPy 2.x
- Pygame CE 2.x (solo para la vista)

En Windows, desde esta carpeta:

```powershell
python -m pip install numpy pygame-ce
python -m neurito_ecosistema.experimentos
python -m neurito_ecosistema.visualizar
```

El primer comando de experimentos entrena y guarda pesos en `modelos/`, y deja los datos en `evidencia/`. La vista crea los modelos si todavía no existen.

## Diseño

El mundo es una cuadrícula 24×24. Las presas buscan alimento, evitan depredadores y pierden energía; los depredadores persiguen presas, pierden energía y recuperan energía al capturarlas. Hay tres escenarios: abundancia, escasez y presión (más depredadores y obstáculos).

Cada especie usa una MLP 6→32→24→9 con ReLU en capas ocultas y Softmax en la salida. Las seis entradas codifican dirección unitaria al objetivo primario, dirección secundaria (amenaza para presa o comida para depredador), energía y disponibilidad de objetivo. Las nueve salidas son los ocho movimientos y quedarse quieto. La decisión de movimiento se toma mediante argmax de la salida neuronal.

El entrenamiento es supervisado: un experto vectorial genera etiquetas, y la red aprende a imitarlo mediante entropía cruzada y descenso de gradiente por mini lotes. Las reglas expertas son referencia y fuente de etiquetas, no sustituyen las decisiones neuronales en la política entrenada. El alcance no es aprendizaje por refuerzo ni evolución.

## Experimentos reproducibles

`experimentos.py` corre 10 semillas por escenario y compara red entrenada, red sin entrenar, política experta de reglas y política aleatoria (120 episodios). Registra supervivientes, alimento consumido, capturas, energía media y tiempo hasta primera captura. Incluye desviación estándar de las métricas y una comparación 16–12 frente a 32–24 neuronas ocultas en `modelos/training_summary.json`. También registra pérdida y precisión antes/después del entrenamiento sobre una partición de prueba. Semilla de generación/entrenamiento: 42; semillas de episodio: 1000–1009; horizonte: 250 pasos.

Los resultados son descriptivos de este modelo y estas semillas. Las etiquetas derivadas de una regla no constituyen evidencia de que la red haya aprendido una estrategia mejor que esa regla; la comparación conductual con líneas base permite ver cuándo se aproxima y dónde falla.

## Vista

`visualizar.py` abre Pygame. ESPACIO inicia/pausa; flecha derecha avanza un paso; N cambia escenario; P alterna política neuronal, aleatoria y reglas; R reinicia; ESC cierra. El panel muestra poblaciones, consumo, capturas, energía y una decisión neuronal de muestra.

## Archivos

- `neurito_ecosistema/`: entorno, MLP, entrenamiento, experimentos y vista.
- `modelos/`: pesos entrenados reproducibles.
- `evidencia/`: datos por episodio y resúmenes generados.
- `INFORME_TECNICO.docx` y `INFORME_TECNICO.pdf`: informe listo para revisar o entregar.\n- `INFORME_TECNICO.md`: fuente editable del informe.
- `BITACORA_DECISIONES.md`: decisiones justificadas.

## Uso de IA

Se utilizó un asistente de programación para estructurar y redactar componentes. El equipo debe revisar el código, ejecutar los experimentos, comprender la retropropagación y declarar qué cambios aceptó o rechazó antes de la sustentación.

