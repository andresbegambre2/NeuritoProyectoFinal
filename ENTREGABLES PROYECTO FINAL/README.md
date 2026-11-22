# Entrega final del NeuroEcosistema

Aquí está el informe final en PDF, la bitácora de decisiones y los archivos para revisar los experimentos. El código y las instrucciones para ejecutar la simulación están en la carpeta principal del repositorio.

## Contenido

- `INFORME_TECNICO.pdf`: informe final (cuatro páginas).
- `BITACORA_DECISIONES.md`: nueve decisiones del proyecto, con alternativas y razones.
- `evidencia/episodios.csv`: resultados de los 360 episodios.
- `evidencia/resumen.csv` y `resumen.json`: promedios y comparaciones.
- `evidencia/graficas/`: gráficas de supervivencia y entrenamiento.
- `modelos/`: pesos de las dos redes y resumen del entrenamiento.

La política aleatoria dejó más presas vivas en los tres escenarios. El informe explica este resultado, las limitaciones de la comparación y el uso de Codex como apoyo de programación.

Para ejecutar la aplicación, abre PowerShell en la carpeta principal del repositorio, instala las dependencias de `requirements.txt` y ejecuta `python -m neurito_ecosistema.visualizar`. En Windows también puedes abrir `INICIAR_SIMULACION.bat`.
