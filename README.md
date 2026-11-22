# NeuroEcosistema Neurito

Este proyecto simula presas y depredadores en un tablero de 24 × 24. Cada población puede moverse con una red neuronal, una regla fija o una política aleatoria. La idea fue comparar esas opciones en distintos escenarios y guardar resultados que permitan revisar las conclusiones.

## Ejecutar en Windows

Abre PowerShell en la carpeta principal del repositorio: es la que contiene `requirements.txt`, `INICIAR_SIMULACION.bat` y `neurito_ecosistema/`. Ejecuta:

```powershell
python -m pip install -r requirements.txt
python -m neurito_ecosistema.visualizar
```

La ventana aparece pausada. Para iniciarla, presiona **Espacio**. Si ya están instaladas las dependencias, también puedes abrir `INICIAR_SIMULACION.bat`.

Para volver a entrenar las redes y regenerar los experimentos, ejecuta:

```powershell
python -m neurito_ecosistema.experimentos
```

Esto vuelve a guardar los modelos y los archivos de `evidencia/`. No hace falta correrlo para mostrar la aplicación: los modelos y los resultados actuales ya están incluidos.

## Cómo está hecha la simulación

Cada episodio empieza con 12 presas. Se puede cambiar entre tres escenarios: abundancia (22 alimentos y 2 depredadores), escasez (7 alimentos y 2 depredadores) y presión (16 alimentos, 5 depredadores y 18 obstáculos). Las poblaciones consumen energía al moverse y la recuperan al comer o capturar. Un episodio termina cuando se extingue una población o llega al máximo de 250 pasos.

Hay una red neuronal MLP para cada especie. Cada red tiene dos capas ocultas, usa ReLU y Softmax, y selecciona una de nueve acciones: ocho movimientos o quedarse quieta. Las entradas representan direcciones hacia objetivos cercanos, energía y disponibilidad de objetivos. En el modelo de depredador se incluye una dirección hacia el alimento, aunque la regla usada para generar las etiquetas de entrenamiento no aprovecha esa entrada; es una limitación que se explica en el informe.

El entrenamiento es supervisado: las redes aprenden a imitar las decisiones de una regla vectorial. No es aprendizaje por refuerzo. Por eso, una exactitud alta muestra que la red aprendió a copiar esa regla, pero no demuestra por sí misma que el ecosistema mejore.

## Qué se comparó

Los experimentos prueban cuatro políticas: red entrenada, la misma red antes de entrenar, reglas y movimiento aleatorio. Cada política se aplica tanto a las presas como a los depredadores. Se hicieron 30 repeticiones por política y escenario, con semillas emparejadas de 1000 a 1029: 360 episodios en total. Se registraron presas supervivientes, alimento consumido, capturas, energía, duración y motivo de finalización.

En estos resultados, la política aleatoria dejó más presas vivas en los tres escenarios. La red entrenada se pareció a la regla experta y logró más capturas. No se presenta la red como superior en supervivencia: los datos no muestran eso. El informe también explica que, al cambiar la política de las dos especies a la vez, no se puede aislar cuál de ellas produjo la diferencia.

## Controles de la ventana

- **Espacio:** iniciar o pausar.
- **Flecha derecha:** avanzar un paso mientras está pausada.
- **N:** cambiar de escenario.
- **P:** alternar entre política neuronal, aleatoria y de reglas.
- **R:** reiniciar el escenario.
- **Esc:** salir.

## Archivos principales

- `neurito_ecosistema/`: simulación, redes, entrenamiento, experimentos y ventana gráfica.
- `modelos/`: pesos entrenados y resumen del entrenamiento.
- `evidencia/`: datos de cada episodio, resúmenes y gráficas.
- `ENTREGABLES PROYECTO FINAL/`: informe, bitácora, auditoría y copia organizada de los resultados.

El informe tiene cuatro páginas. La bitácora documenta nueve decisiones técnicas. Los CSV permiten consultar los resultados por episodio y sus resúmenes.

## Apoyo de programación

Desarrollé el proyecto con apoyo de Codex, un asistente de programación. Lo usé para revisar y completar parte del código, organizar las pruebas y preparar la documentación. Yo revisé la propuesta y ejecuté la aplicación en mi computador. Acepté ayuda para organizar la comparación de políticas; no tomé la exactitud de imitación como prueba de que la red mejorara la supervivencia, porque los resultados muestran lo contrario. Las cifras del informe se contrastaron con los CSV y el resumen de entrenamiento. Debo poder explicar las decisiones, los resultados y las limitaciones durante la sustentación.
